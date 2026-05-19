from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Track, UserProfile
from ranged_response import RangedFileResponse

import os
def home_page(request):
    query = request.GET.get('q', '')
    tracks = Track.objects.all().select_related('band')

    if query:
        tracks = tracks.filter(
            Q(title__icontains=query) | Q(band__name__icontains=query)
        )

    return render(request, 'music/home.html', {'tracks': tracks, 'query': query})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "music/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "music/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")

@login_required(login_url='login')
def favorites_page(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    tracks = profile.favorite_tracks.all()
    return render(request, 'music/home.html', {'tracks': tracks, 'is_favorites_page': True})

@login_required(login_url='login')
def toggle_favorite(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if track in profile.favorite_tracks.all():
        profile.favorite_tracks.remove(track)
    else:
        profile.favorite_tracks.add(track)
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def stream_audio(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    file_path = track.audio_file.path
    
    file = open(file_path, 'rb')
    response = RangedFileResponse(request, file, content_type='audio/mpeg')
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response