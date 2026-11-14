"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from project7 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.RoomListView.as_view(), name="home"),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('booking/<int:pk>/cancel/', views.CancelBookingView.as_view(), name='cancel_booking'),
    path('book/<int:room_id>/', views.BookingCreateView.as_view(), name='book_room'),
    path("rooms/<int:room_id>/", views.RoomDetailView.as_view(), name="room_detail"),
    path("rooms/<int:room_id>/availability/", views.room_availability, name="room_availability"),
]

