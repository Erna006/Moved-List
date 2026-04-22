import django_filters
from .models import Film


class FilmFilter(django_filters.FilterSet):
    """
    Filters for films with the ability to filter by:
    - Genre
    - Country
    - Language
    - Year (exact match and range)
    - Rating (minimum)
    """
    
    genre = django_filters.NumberFilter(field_name='genres', lookup_expr='exact')
    genres = django_filters.BaseInFilter(field_name='genres', lookup_expr='in')
    
    country = django_filters.NumberFilter(field_name='countries', lookup_expr='exact')
    countries = django_filters.BaseInFilter(field_name='countries', lookup_expr='in')
    
    language = django_filters.NumberFilter(field_name='languages', lookup_expr='exact')
    languages = django_filters.BaseInFilter(field_name='languages', lookup_expr='in')
    
    year = django_filters.NumberFilter(field_name='year', lookup_expr='exact')
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')
    
    duration_min = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    duration_max = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')
    
    min_rating = django_filters.NumberFilter(method='filter_by_rating')
    
    class Meta:
        model = Film
        fields = {
            'year': ['exact', 'gte', 'lte'],
            'duration': ['gte', 'lte'],
        }
    
    def filter_by_rating(self, queryset, name, value):
        """
        Filters films by minimum average rating
        """
        from django.db.models import Avg
        
        return queryset.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=value)