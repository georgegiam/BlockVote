from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),    
    path('cast_vote', views.votingNow, name="vote"),
    path('check_vote', views.checkingNow, name="check"),
    
    path('cast_vote/api/vote', views.cast_vote, name="cast_vote"),
    path('check_vote/api/check', views.check_vote, name="check_vote"),
    
]
