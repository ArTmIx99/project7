from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Room, Booking
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookingForm, RegisterForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from django.utils.http import url_has_allowed_host_and_scheme

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


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    def dispatch(self, request, *arcs, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().dispatch(request, *arcs, **kwargs)
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        next_url = self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={self.request.get_host()}):
            return redirect(next_url)
        return redirect("home")

class ProfileView(LoginRequiredMixin, ListView):
    template_name = "project7/profile.html"
    context_object_name = "bookings"
    def get_queryset(self):
        return (
            Booking.objects
            .filter(user = self.request.user)
            .select_related("room", "room__room_type")
            .order_by("-start_date")
        )

class CancelBookingView(LoginRequiredMixin, View):
    def post(self, request, pk):
        booking = get_object_or_404(Booking, pk = pk, user = request.user)
        if booking.status != "cancelled":
            booking.status = "cancelled"
            booking.save()
        return redirect("profile")