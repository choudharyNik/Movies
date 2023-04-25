from django.contrib import admin
from movies.models import Movie, MovieCast, Genre

# Register your models here.
admin.site.register(Movie)
admin.site.register(MovieCast)
admin.site.register(Genre)