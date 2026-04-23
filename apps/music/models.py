from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Band(models.Model):
    name = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='bands/', blank=True)

    def __str__(self):
        return self.name

class Track(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='tracks/')
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='tracks')
    duration = models.DurationField(null=True, blank=True)
    play_count = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.band.name} - {self.title}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_tracks = models.ManyToManyField(Track, blank=True, related_name='favorited_by')

class Playlist(models.Model):
    title = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    tracks = models.ManyToManyField(Track, through='PlaylistTrack')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ['position']

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='ratings')
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class PlaybackHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    played_at = models.DateTimeField(auto_now_add=True)

class Donation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_band = models.ForeignKey(Band, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)