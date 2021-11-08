from django.contrib import admin

from .models import Bookings, Contacts, Albums, Artists


class BookingsInline(admin.TabularInline):
    model = Bookings
    fieldsets = [(None, {'fields': ['album', 'has_been_contacted']})]
    extra = 0
    verbose_name = 'Réservation'
    verbose_name_plural = 'Réservations'


class AlbumArtistsInline(admin.TabularInline):
    model = Albums.artists.through
    extra = 1
    verbose_name = 'Album'
    verbose_name_plural = 'Albums'


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'has_been_contacted']


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    inlines = [BookingsInline, ]


@admin.register(Artists)
class ArtistsAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistsInline, ]

@admin.register(Albums)
class AlbumsAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']
