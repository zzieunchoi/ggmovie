from django.db import models
from django.conf import settings
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()
    release_date = models.DateField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    genres = models.ManyToManyField(Genre)
    poster_path = models.TextField()
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name = 'like_movie')
    
    def __str__(self):
        return self.title

class MovieComment(models.Model):
    title = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rank = models.IntegerField()
    updated_at = models.DateTimeField(auto_now = True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content