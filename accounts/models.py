from django.contrib.auth.models import AbstractUser
from django.db import models
# from movies.models import Genre

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Award(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="닉네임")
    favorite_directors = models.ManyToManyField('Director', blank=True)
    favorite_genres = models.ManyToManyField('movies.Genre', related_name='favorite_users', blank=True)
    favorite_awards = models.ManyToManyField('Award', blank=True)
    birth_date = models.DateField(null=True, blank=True)  # 생년월일 추가
    email = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.username