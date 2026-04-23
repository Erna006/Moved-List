from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ['name']

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    photo = models.ImageField(upload_to='actors/photos/', blank=True, null=True)
    bio = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'
        ordering = ['name']

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2026)])
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    poster = models.ImageField(upload_to='posters/')
    trailer_url = models.FileField(upload_to='trailers/', blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name='films')
    countries = models.ManyToManyField(Country, related_name='films')
    languages = models.ManyToManyField(Language, related_name='films')
    actors = models.ManyToManyField(Actor, through='FilmActor', related_name='films',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Films"
        ordering = ['-year', 'title']
        indexes = [
            models.Index(fields=['year']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    @property
    def average_rating(self):
        avg = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0
    
    @property
    def reviews_count(self):
        return self.reviews.count()


class FilmActor(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    role = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "Actor in film"
        verbose_name_plural = "Actors in films"
        ordering = ['order', 'actor__name']
        unique_together = ['film', 'actor']
    
    def __str__(self):
        return f"{self.actor.name} in {self.film.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ['-created_at']
        unique_together = ['user', 'film']
        indexes = [
            models.Index(fields=['film', '-created_at']),
        ]
    
    def __str__(self):
        return f"Review by {self.user.username} on {self.film.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"
        ordering = ['-added_at']
        unique_together = ['user', 'film']
    
    def __str__(self):
        return f"{self.user.username} - {self.film.title}"
