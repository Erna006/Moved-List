from django.contrib import admin
from .models import (
    Film, Genre, Country, Language, Actor,
    FilmActor, Review, Favorite
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']
    list_filter = ['code']


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo']
    search_fields = ['name']
    list_filter = ['name']


class FilmActorInline(admin.TabularInline):
    """Inline to add actors to a film"""
    model = FilmActor
    extra = 1
    autocomplete_fields = ['actor']


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'duration', 'trailer_url', 'average_rating', 'created_at']
    list_filter = ['year', 'genres', 'countries', 'languages']
    search_fields = ['title', 'description']
    filter_horizontal = ['genres', 'countries', 'languages']
    inlines = [FilmActorInline]
    readonly_fields = ['average_rating', 'reviews_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Main information', {
            'fields': ('title', 'description', 'year', 'duration', 'trailer_url', 'poster')
        }),
        ('Categories', {
            'fields': ('genres', 'countries', 'languages')
        }),
        ('Statistics', {
            'fields': ('average_rating', 'reviews_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'film', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'film__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    def has_change_permission(self, request, obj=None):
        """Admins can edit any reviews"""
        return True


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'film', 'added_at']
    list_filter = ['added_at']
    search_fields = ['user__username', 'film__title']
    readonly_fields = ['added_at']