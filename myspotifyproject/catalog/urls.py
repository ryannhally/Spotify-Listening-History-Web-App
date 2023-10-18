from django.urls import path
from . import views
from .views import login_spotify

urlpatterns = [
    path('catalog/', views.welcome, name="welcome"),
    path('login/', views.login_spotify, name="login"),
    path('callback/', views.get_token, name="token"),
    path('toptracks/', views.get_more_tracks, name="tracks"),
    path('topartists/', views.get_more_artists, name="artists")
]
