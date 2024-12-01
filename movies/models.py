from django.db import models
from accounts.models import User

class Genre(models.Model):
    name = models.CharField(max_length=255)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)  # NULL 허용으로 변경

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=255)
    character = models.CharField(max_length=255, null=True, blank=True)
    profile_path = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} as {self.character}"

class Movie(models.Model):
    like_users = models.ManyToManyField(User, related_name='like_movies')
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    runtime = models.IntegerField(null=True, blank=True)
    age_rating = models.CharField(max_length=50, null=True, blank=True)
    overview = models.TextField(null=True, blank=True)
    poster_path = models.CharField(max_length=255, null=True, blank=True)
    director = models.CharField(max_length=255, null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    weather = models.JSONField(null=True, blank=True)
    recommended_temperature = models.JSONField(
        default=list,
        blank=True,
        null=True,
    )  # 추천 온도를 리스트 형태로 저장. 예: ["hot", "cold"]

    def __str__(self):
        return self.title

class MovieComment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
