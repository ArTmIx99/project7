from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import Room, Booking, RoomType
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import BookingForm, RegisterForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login
from django.utils.http import url_has_allowed_host_and_scheme
from django.http import JsonResponse
from django.utils.dateparse import parse_date

class RoomListView(ListView):
    model = Room
    template_name = "project7/room_list.html"
    context_object_name = "rooms"

    def get_queryset(self):
        qs = Room.objects.select_related("room_type")
        type_id = self.request.GET.get("type")
        if type_id and type_id.isdigit():
            qs = qs.filter(room_type_id = type_id)
        start = parse_date(self.request.GET.get("start") or"" )
        end = parse_date(self.request.GET.get("end") or"" )
        if start and end and start < end:
            busy_room_ids = (
                Booking.objects
                .filter(start_date__date__lt=end, end_date__date__gt=start)
                .exclude(status = "cancelled")
                .values("room_id")
            )
            qs = qs.exclude(id__in = busy_room_ids)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["room_types"] = RoomType.objects.all()
        ctx["selected_type"] = self.request.GET.get("type", "")
        ctx["start"] = self.request.GET.get("start", "")
        ctx["end"] = self.request.GET.get("end", "")
        return ctx
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
        ).exclude(status = "cancelled")
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


class RoomDetailView(DetailView):
    model = Room
    template_name = "project7/room_detail.html"
    context_object_name = "room"
    pk_url_kwarg = "room_id"


def room_availability(request, room_id):
    bookings = (
        Booking.objects
        .filter(room_id=room_id)
        .exclude(status="cancelled")
    )
    events = [
        {
            "title": "Зайнято" if b.status == "confirmed" else "Очікує підтвердження",
            "start": b.start_date.isoformat(),
            "end": b.end_date.isoformat(),
            "color": "#dc3545" if b.status == "confirmed" else "#ffc107",
        }
        for b in bookings
    ]
    return JsonResponse(events, safe=False)