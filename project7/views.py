from django.shortcuts import render
from django.views.generic import ListView
from .models import Room, Booking
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookingForm
from django.shortcuts import get_object_or_404

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

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['room'] = get_object_or_404(Room, id = self.kwargs['room_id'])
        return context


    def form_valid(self, form):
        room = get_object_or_404(Room, id = self.kwargs['room_id'])
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        overlaps = Booking.objects.filter(
            room = room,
            start_date__lt = end,
            end_date__gt = start
        )
        if overlaps.exists():
            form.add_error(None, "Ці дати вже зайняті")
            return self.form_invalid(form)
        form.instance.user = self.request.user
        form.instance.room = room
        return super().form_valid(form)
    
