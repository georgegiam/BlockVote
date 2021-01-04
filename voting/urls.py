from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('voting', views.votingNow, name="vote"),
    path('test', views.some_view, name="some_view"),
    path('vote', views.cast_vote, name="cast_vote"),
    path('check', views.check_vote, name="check_vote"),
    
]
