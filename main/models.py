from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=300)
    tagline = models.CharField(max_length=300, default='')
    genres = models.ManyToManyField(Genre)
    director = models.CharField(max_length=300)
    cast = models.CharField(max_length=800)
    description = models.TextField(max_length=5000)
    release_date = models.DateField()
    average_rating = models.FloatField(default=0)
    image = models.URLField(default=None, null=True)
    video_url = models.URLField('Video URL', default=None, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.user.username