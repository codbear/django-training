from django.db import models


class Artits(models.Model):
    name = models.CharField(max_length=200, unique=True)
