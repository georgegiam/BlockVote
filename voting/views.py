import re
import voting.blockchain_voting_system as bvs
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

voter_id_set = set()
c = bvs.MinimalChain()
# get the set of super_users: (<User: sk>, <User: Matty>)
super_users = User.objects.filter(is_superuser=True)

# Views
#login
def home(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            loguser=request.user
            request.session['username'] = str(username)
            print(request.session['username'])
            return render(request, 'voting/index.html')
        else:
            return render(request,"voting/login.html", { 'message': 'true'})
    else:
        return render(request,"voting/login.html")

def mylogout(request):
    print(request.session['username'])
    logout(request)
    request.session['username']=None
    print(request.session['username'])
    return redirect('../login/')

# index
def index(request):
    return render(request, 'voting/index.html')

# voting
def votingNow(request):
    return render(request, 'voting/vote.html')

#checking
def checkingNow(request):
    return render(request, 'voting/check.html')

#main api call to cast vote
@method_decorator(csrf_exempt, name='dispatch')
def cast_vote(request):
         
    voter_id = request.POST.get('voter_id', '')
    candidate_id = request.POST.get('candidate_id', '')

    pattern_voter_id = '\d{1,9}'
    pattern_candidate_id = '[1-9]'

    result_voter = re.match(pattern_voter_id, voter_id)
    result_candidate = re.match(pattern_candidate_id, candidate_id)

    if result_voter and result_candidate:
        if voter_id not in voter_id_set:

            voter_id_set.add(voter_id)

            c.add_block('{},{}'.format(voter_id,candidate_id))
            # print("voting successful.")
            return render(request, 'voting/success.html')
        else:
            print("voting unsuccessful.")
            # return JsonResponse({'error': 'already voted once!'}, status=422)
            return render(request, 'voting/error_twice.html')
    else:
        print("voting unsuccessful.")
        # return JsonResponse({'error': 'malformed params, check voting documentation!'}, status=422)
        return render(request, 'voting/error_input.html')

@method_decorator(csrf_exempt, name='dispatch')
def check_vote(request):
    
    voter_id = request.POST.get('voter_id', '')
    pattern_voter_id = '\d{1,9}'
    
    result_voter = re.match(pattern_voter_id, voter_id)

    if result_voter:
        
        block_list = c.blocks
        if len(block_list) > 1:
            for block in block_list:
                data = block.data
                try:
                    block_voter_id, block_candidate = data.split(',')
                except:
                    block_voter_id = ''
                    block_candidate = ''
                    print(data)
                if block_voter_id == voter_id:
                    args = {}
                    args['cand'] = block_candidate
                    args['voter'] = voter_id
                    # return JsonResponse({'candidate_id': block_candidate})
                    return render(request, 'voting/my_vote.html', args)

        # return JsonResponse({'error': 'vote not found!'}, status=404)
        return render(request, 'voting/error_user.html')
    else:
        print("check unsuccessful.")
        # return JsonResponse({'error': 'malformed params, check voting documentation!'}, status=422)
        return render(request, 'voting/error_input.html')


@method_decorator(csrf_exempt, name='dispatch')
def count_votes(request):
    # if request.session['username'] is not None:
        count_candidate = {
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 0,
            '9': 0,
        }
        if c.get_chain_size() > 0:
            for block in c.blocks[1:]:
                data = block.data.split(',')
                candidate_id = data[1].strip()
                count_candidate[candidate_id] += 1

            winner_id = max(count_candidate, key=count_candidate.get)
            context = {
                "Winner": winner_id,
            }
            return render(request, "voting/show_winner.html", context)
        else:
            context = {
                "Error": "The chain is empty.",
            }
            return render(request, "voting/show_winner.html", context)
    # else:
    #     return render(request, "voting/error_user.html")


def display_chain(request):
    """
    :param request:
    :return: A list of MiniBlock().
            Error if the blockchain is empty.
    """
    if c.get_chain_size() > 0:
        data = []
        timestamps = []
        for block in c.blocks[1:]:
            data.append(block.data)
            timestamps.append(block.timestamp.strftime("%Y-%m-%d  %H:%M:%S"))

        context = {}
        context['data'] = data
        context['timestamps'] = timestamps
        return render(request, "voting/show_chain.html", context)
    else:
        context = {
            "Error": "The chain is empty."
        }
        return render(request, "voting/show_chain.html", context)