from django.shortcuts import render
from django.views.generic import ListView
from .models import Room, Booking
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookingForm

class RoomListView(ListView):
    model = Room
    template_name = "project7/room_list.html"
    context_object_name = "rooms"
# Create your views here.
class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "project7/booking_form.html"
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
