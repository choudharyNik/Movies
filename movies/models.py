from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=150)
    overview = models.CharField(max_length=1000)
    tagline = models.CharField(max_length=250)
    release_date = models.DateField(_("release date"))
    vote_average = models.FloatField(_("average vote"))
    vote_count = models.BigIntegerField(_("vote count"))
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

class MovieCast(models.Model):
    character_name = models.CharField(_("character name"), max_length=100)
    cast_name = models.CharField(_("cast name"), max_length=100)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)

    def __str__(self):
        return self.character_name + ' - ' + self.cast_name



