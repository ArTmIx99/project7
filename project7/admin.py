from django.contrib import admin, messages
from .models import Room, Booking, RoomType
# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("title", "room_type", "price", "capacity")
    list_filter = ("room_type",)
    search_fields = ("title", "description")
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "user", "start_date", "end_date", "status")
    list_filter = ("status", "room__room_type", "room", "start_date")
    search_fields = ("user__username", "user__email", "room__title")
    list_select_related = ("room", "user")
    list_editable = ("status",)
    date_hierarchy = "start_date"
    ordering = ("-start_date",)
    actions = ["confirm_bookings", "cancel_bookings"]
    @admin.action(description="Підтвердити вибрані бронювання")
    def confirm_bookings(self, request, queryset):
        updated = queryset.exclude(status="cancelled").update(status="confirmed")
        self.message_user(request, f"Підтверджено: {updated}", messages.SUCCESS)

    @admin.action(description="Скасувати вибрані бронювання")
    def cancel_bookings(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"Скасовано: {updated}", messages.WARNING)
    

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)