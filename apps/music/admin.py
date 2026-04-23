from django.contrib import admin
from .models import Band, Track, UserProfile, Playlist, PlaylistTrack, Rating, PlaybackHistory, Donation

admin.site.register(Band)
admin.site.register(Track)
admin.site.register(UserProfile)
admin.site.register(Playlist)
admin.site.register(PlaylistTrack)
admin.site.register(Donation)