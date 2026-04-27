from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('favorites/', views.favorites_page, name='favorites'),
    path('toggle-favorite/<int:track_id>/', views.toggle_favorite, name='toggle_favorite'),
]