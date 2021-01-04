from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),    
    path('vote', views.votingNow, name="vote"),
    
    path('api/vote', views.cast_vote, name="cast_vote"),
    path('api/check', views.check_vote, name="check_vote"),
    
]
