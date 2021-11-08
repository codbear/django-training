from django.test import TestCase
from django.urls import reverse

from .models import Albums, Contacts, Artists, Bookings


class IndexPageTestCase(TestCase):
    def test_index_page_returns_200(self):
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)


class SinglePageTestCase(TestCase):
    def setUp(self) -> None:
        album = Albums.objects.create(title='Golden')
        self.album_id = Albums.objects.get(title='Golden').id

    def test_single_page_returns_200_if_album_is_found(self):
        album_id = self.album_id

        response = self.client.get(reverse('store:single', args=(album_id,)))

        self.assertEqual(response.status_code, 200)

    def test_single_page_returns_404_if_album_is_not_found(self):
        album_id = self.album_id + 1

        response = self.client.get(reverse('store:single', args=(album_id,)))

        self.assertEqual(response.status_code, 404)


class BookingPageTestCase(TestCase):
    def setUp(self):
        Contacts.objects.create(name="Freddie", email="fred@queen.forever")
        impossible = Albums.objects.create(title="Transmission Impossible")
        journey = Artists.objects.create(name="Journey")
        impossible.artists.add(journey)
        self.album = Albums.objects.get(title='Transmission Impossible')
        self.contact = Contacts.objects.get(name='Freddie')

    def test_new_booking_is_registered(self):
        old_bookings = Bookings.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:single', args=(album_id,)), {
            'name': name,
            'email': email
        })
        new_bookings = Bookings.objects.count()
        self.assertEqual(new_bookings, old_bookings + 1)