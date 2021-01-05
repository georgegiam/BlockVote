from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="index"), 
    path('', views.index, name="index"),  
    path('login/', views.home, name="home"), 
    path('logout/login/', views.home, name="home"), 
    path('logout/', views.mylogout, name="logout"),
    path('cast_vote', views.votingNow, name="vote"),
    path('check_vote', views.checkingNow, name="check"),

    path('countvotes/', views.count_votes, name="countvote"),
    path('dispchain/', views.display_chain, name="displaychain"),
    
    path('cast_vote/api/vote', views.cast_vote, name="cast_vote"),
    path('check_vote/api/check', views.check_vote, name="check_vote"),
    
]
