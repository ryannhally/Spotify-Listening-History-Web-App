from django.urls import path
from . import views
from .views import login_spotify

urlpatterns = [
    path('catalog/', views.welcome),
    path('login/', views.login_spotify, name="login"),
    path('callback/', views.get_token, name="token"),
    path('tracks/', views.get_top_tracks, name='tracks')
]
