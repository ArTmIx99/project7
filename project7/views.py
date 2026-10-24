from django.shortcuts import render
from django.views.generic import ListView
from .models import Room, Booking

class RoomListView(ListView):
    model = Room
    template_name = "project7/room_list.html"
    context_object_name = "rooms"
# Create your views here.
