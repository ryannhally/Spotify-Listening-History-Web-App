from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
import spotipy
import sp
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import requests
from urllib.parse import urlencode
import base64
import credentials



""" 
Renders first page user sees 
"""
def welcome(request):
    return render(request, 'welcome.html')


""" 
Handles 
"""
def login_spotify(request):

    # Headers
    auth_headers = {
    "client_id": credentials.CLIENT_ID,
    "response_type": 'code',
    "redirect_uri": credentials.REDIRECT_URI,
    "scope": credentials.SCOPE
    }

    # URL
    URL = 'https://accounts.spotify.com/authorize?' + urlencode(auth_headers)

    # Redirects user to Spotify login page
    return HttpResponseRedirect(URL)


""" 
Retrieves and stores access token
"""
def get_token(request):

    # Create Spotify OAuth object
    oauth = SpotifyOAuth(client_id=credentials.CLIENT_ID, client_secret=credentials.CLIENT_SECRET, redirect_uri=credentials.REDIRECT_URI, scope=credentials.SCOPE)

    # Get code from return URL
    code = request.GET.get('code')

    # Get access token
    response = oauth.get_access_token(code)

    # Store access token
    acess_token = response["access_token"]

    # Store token in session
    request.session["access_token"] = token

    # Calls method that renders website 
    return get_top_tracks(request)

def get_top_tracks(request):

    token = request.session.get("access_token")

    user_headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    user_params = {
        "limit": 10
    }

    user_tracks_response = requests.get("https://api.spotify.com/v1/me/tracks", params=user_params, headers=user_headers)
   
    print(user_tracks_response.json())


    return render(request, "fake.html")
    """ user_headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json"  
    }

    user_params = {
    "limit": 50
     }

    user_tracks_response = requests.get("https://api.spotify.com/v1/me/tracks", params=user_params, headers=user_headers) """
