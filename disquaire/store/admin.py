from django.contrib import admin

from .models import Bookings


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    pass
