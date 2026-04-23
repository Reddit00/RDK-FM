from django.shortcuts import render
from .models import Track

def home_page(request):
    tracks = Track.objects.all().select_related('band')
    return render(request, 'music/home.html', {'tracks': tracks})