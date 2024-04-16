from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import requests
from urllib.parse import urlencode
import base64
from .  import credentials
import json
from . import get_stats



""" 
Renders first page user sees 
"""
def welcome(request):
    return render(request, 'welcome.html')


""" 
Sends user authorization request
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
    access_token = response["access_token"]

    # Store token in session
    request.session["access_token"] = access_token

    # Calls method that renders first page
    return render(request, "first-page.html")


""" 
Renders first page where user can choose what data to see
"""
def first_page(request):

    # Render first page
    return render(request, "first-page.html")


""" 
Calls method for gathering user's top tracks and renders page that displays them
"""
def get_more_tracks(request):
    
    # Call method to get user's top 25 tracks
    top_25_tracks = get_stats.get_25_tracks(request)
       
    # Context
    context = {
        "top_tracks_names": top_25_tracks[0],
        "top_tracks_artists": top_25_tracks[1],
        "top_tracks_images": top_25_tracks[2]
        }


    # Render page that displays top tracks
    return render(request, "top-tracks.html", context)


""" 
Calls method for gathering user's top artists and renders page that displays them
"""
def get_more_artists(request):
        
     # Call method to get user's top 25 artists
    top_25_artists = get_stats.get_25_artists(request)

       
    # Context
    context = {
        "top_artists_names": top_25_artists[0][0],
        "top_artists_images": top_25_artists[1][0]
        }

    # Render page that displays top artists
    return render(request, "top-artists.html", context)


""" 
Calls method for gathering averages of audio features of user's top songs and renders page that displays them 
"""
def get_audio_features(request):
    
    # Call method to get audio analysis on user's top 25 tracks
    avg_features = get_stats.get_average_features(request)

    # Context
    context = {
        "avg_acousticness": avg_acousticness,
        "avg_danceability": avg_danceability,
        "avg_energy": avg_energy,
        "avg_tempo": avg_tempo
        
    }

    return render(request, "audio-features.html", context )
