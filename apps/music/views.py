from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Track, UserProfile

# 1. Головна сторінка та пошук
def home_page(request):
    query = request.GET.get('q', '')
    tracks = Track.objects.all().select_related('band')

    # Якщо є пошуковий запит - фільтруємо треки
    if query:
        tracks = tracks.filter(
            Q(title__icontains=query) | Q(band__name__icontains=query)
        )

    return render(request, 'music/home.html', {'tracks': tracks, 'query': query})

# 2. Реєстрація користувача
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Створюємо профіль для збереження улюблених треків
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "music/register.html", {"form": form})

# 3. Вхід
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

# 4. Вихід
def logout_view(request):
    logout(request)
    return redirect("home")

# 5. Сторінка "Улюблені треки"
@login_required(login_url='login')
def favorites_page(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    tracks = profile.favorite_tracks.all()
    # Перевикористовуємо home.html, але з прапорцем is_favorites_page
    return render(request, 'music/home.html', {'tracks': tracks, 'is_favorites_page': True})

# 6. Додавання/Видалення з улюблених
@login_required(login_url='login')
def toggle_favorite(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Логіка "лайка" (якщо є - забираємо, якщо немає - додаємо)
    if track in profile.favorite_tracks.all():
        profile.favorite_tracks.remove(track)
    else:
        profile.favorite_tracks.add(track)
        
    # Повертаємо користувача на ту сторінку, де він натиснув кнопку
    return redirect(request.META.get('HTTP_REFERER', 'home'))