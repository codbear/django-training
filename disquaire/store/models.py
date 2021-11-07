from django.db import models


class Artists(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Contacts(models.Model):
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=200)


class Albums(models.Model):
    reference = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    picture = models.URLField()
    artists = models.ManyToManyField(Artists, related_name='albums', blank=True)


class Bookings(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    has_been_contacted = models.BooleanField(default=False)
    album = models.OneToOneField(Albums, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE)
