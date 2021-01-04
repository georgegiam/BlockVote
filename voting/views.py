import re
import voting.blockchain_voting_system as bvs
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

voter_id_set = set()
c = bvs.MinimalChain()

# Views

# index
def index(request):
    return render(request, 'voting/index.html')

# voting
def votingNow(request):
    return render(request, 'voting/vote.html')

#test view
def some_view(request):
    return JsonResponse({'world': 'earth', 'status': 'hello'})

#main api call to cast vote
@method_decorator(csrf_exempt, name='dispatch')
def cast_vote(request):
    
    if request.method == 'POST':        
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
            print("voting successful.")
            
            return JsonResponse({'user_voter_id': voter_id, 'candidate_id': candidate_id, 'voting_status':'successful'})
        else:
            print("voting unsuccessful.")
            return JsonResponse({'error': 'already voted once!'}, status=422)
    else:
        print("voting unsuccessful.")
        return JsonResponse({'error': 'malformed params, check voting documentation!'}, status=422)

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
                    return JsonResponse({'candidate_id': block_candidate})

        return JsonResponse({'error': 'vote not found!'})
        
        
    else:
        print("check unsuccessful.")
        return JsonResponse({'error': 'malformed params, check voting documentation!'}, status=422)


def count_votes():
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
    for block in c.blocks[1:]:
        data = block.data.split(',')
        candidate_id = data[1].strip()
        count_candidate[candidate_id] += 1

    winner_id = max(count_candidate, key=count_candidate.get)
    return JsonResponse({'Winner': winner_id})


def print_block(block):
    print('Block    #', block.index)
    print('          ', block.data)
    print('Timestamp ', block.timestamp)
    print('\n------------\n')


def display_chain():
    for block in c.blocks[1:]:
        print_block(block)

