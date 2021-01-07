from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),  
    path('tutorial', views.tutorial, name='tutorial'),
    path('login/', views.home, name="home"), 
    path('logout/login/', views.home, name="home"), 
    path('logout/', views.mylogout, name="logout"),
    path('cast_vote', views.votingNow, name="vote"),
    path('check_vote', views.checkingNow, name="check"),
    

    path('winner/', views.count_votes, name="countvote"),
    path('showchain/', views.display_chain, name="displaychain"),
    
    path('cast_vote/api/vote', views.cast_vote, name="cast_vote"),
    path('check_vote/api/check', views.check_vote, name="check_vote"),
    
]
