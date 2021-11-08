from django.db import models


class Artists(models.Model):
    name = models.CharField('nom', max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'artiste'


class Contacts(models.Model):
    email = models.EmailField('email', max_length=100)
    name = models.CharField('nom', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'prospect'


class Albums(models.Model):
    reference = models.CharField('référence', max_length=200, null=True)
    created_at = models.DateTimeField('date de création', auto_now_add=True)
    is_available = models.BooleanField('disponible', default=True)
    title = models.CharField('titre', max_length=200)
    picture = models.URLField('pochette')
    artists = models.ManyToManyField(Artists, related_name='albums', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'album'


class Bookings(models.Model):
    created_at = models.DateTimeField('date de création', auto_now_add=True)
    has_been_contacted = models.BooleanField('réservation traitée', default=False)
    album = models.OneToOneField(Albums, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE)

    def __str__(self):
        return self.contact.name

    class Meta:
        verbose_name = 'réservation'
