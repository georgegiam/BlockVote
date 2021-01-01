from django.shortcuts import render
from django.http import HttpResponse

# Views

# index
def index(request):
    return render(request, 'voting/index.html')

