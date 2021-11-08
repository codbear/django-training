from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Bookings, Contacts, Albums, Artists


def get_admin_url(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return reverse('admin:store_%s_change' % content_type.model, args=(obj.id,))


class BookingsInline(admin.TabularInline):
    model = Bookings
    fieldsets = [(None, {'fields': ['album_link', 'has_been_contacted']})]
    readonly_fields = ['created_at', 'album_link', 'has_been_contacted']
    extra = 0
    verbose_name = 'Réservation'
    verbose_name_plural = 'Réservations'

    def has_add_permission(self, request, obj):
        return False

    def album_link(self, booking):
        url = get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))

    album_link.short_description = 'Album'


class AlbumArtistsInline(admin.TabularInline):
    model = Albums.artists.through
    extra = 1
    verbose_name = 'Album'
    verbose_name_plural = 'Albums'


@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_filter = ['created_at', 'has_been_contacted']
    fieldsets = [(None, {'fields': ['created_at', 'contact_link', 'album_link', 'has_been_contacted']})]
    readonly_fields = ['created_at', 'contact_link', 'album_link']

    def has_add_permission(self, request):
        return False

    def contact_link(self, booking):
        url = get_admin_url(booking.contact)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.contact.name))

    contact_link.short_description = 'Prospect'

    def album_link(self, booking):
        url = get_admin_url(booking.album)
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))

    album_link.short_description = 'Album'


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    inlines = [BookingsInline, ]


@admin.register(Artists)
class ArtistsAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistsInline, ]


@admin.register(Albums)
class AlbumsAdmin(admin.ModelAdmin):
    search_fields = ['reference', 'title']
