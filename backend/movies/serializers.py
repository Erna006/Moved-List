from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Film, Genre, Country, Language, Actor, 
    FilmActor, Review, Favorite
)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, trim_whitespace=False)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=False, allow_blank=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'code']


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['id', 'name', 'code']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'name', 'photo', 'bio']


class FilmActorSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    
    class Meta:
        model = FilmActor
        fields = ['actor', 'role', 'order']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_id', 'film', 'rating', 
            'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            user = request.user
            film = data.get('film')
            if Review.objects.filter(user=user, film=film).exists():
                raise serializers.ValidationError(
                    "You have already left a review for this film"
                )
        return data
    
    def create(self, validated_data):
        """Automatically set the user from the request"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FilmListSerializer(serializers.ModelSerializer):
    """Brief serializer for film list"""
    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Film
        fields = [
            'id', 'title', 'year', 'duration', 'poster',
            'genres', 'countries', 'average_rating', 'reviews_count',
            'trailer_url'
        ]


class FilmDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for film details"""
    genres = GenreSerializer(many=True, read_only=True)
    countries = CountrySerializer(many=True, read_only=True)
    languages = LanguageSerializer(many=True, read_only=True)
    film_actors = FilmActorSerializer(
        source='filmactor_set',
        many=True,
        read_only=True
    )
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()
    genre_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    country_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    language_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Film
        fields = [
            'id', 'title', 'description', 'year', 'duration', 'poster', 'trailer_url',
            'genres', 'countries', 'languages', 'film_actors',
            'reviews', 'average_rating', 'reviews_count',
            'created_at', 'updated_at',
            'genre_ids', 'country_ids', 'language_ids'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """Creating film with relationships"""
        genre_ids = validated_data.pop('genre_ids', [])
        country_ids = validated_data.pop('country_ids', [])
        language_ids = validated_data.pop('language_ids', [])
        
        film = Film.objects.create(**validated_data)
        
        if genre_ids:
            film.genres.set(genre_ids)
        if country_ids:
            film.countries.set(country_ids)
        if language_ids:
            film.languages.set(language_ids)
        
        return film
    
    def update(self, instance, validated_data):
        """Updating film with relationships"""
        genre_ids = validated_data.pop('genre_ids', None)
        country_ids = validated_data.pop('country_ids', None)
        language_ids = validated_data.pop('language_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if genre_ids is not None:
            instance.genres.set(genre_ids)
        if country_ids is not None:
            instance.countries.set(country_ids)
        if language_ids is not None:
            instance.languages.set(language_ids)
        
        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for favorite films"""
    film = FilmListSerializer(read_only=True)
    film_id = serializers.PrimaryKeyRelatedField(
        source='film',
        queryset=Film.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Favorite
        fields = ['id', 'film', 'film_id', 'added_at']
        read_only_fields = ['added_at']
    
    def validate(self, data):
        """Check that the film is not already in favorites"""
        request = self.context.get('request')
        if request and request.method == 'POST':
            user = request.user
            film = data.get('film')
            if Favorite.objects.filter(user=user, film=film).exists():
                raise serializers.ValidationError(
                    "This film is already in favorites"
                )
        return data
    
    def create(self, validated_data):
        """Automatically set the user from the request"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']
    
    def validate(self, data):
        """Check that passwords match"""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match'
            })
        if User.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError({
                'email': 'A user with this email already exists'
            })
        try:
            validate_password(data['password'])
        except DjangoValidationError as exc:
            raise serializers.ValidationError({
                'password': list(exc.messages)
            }) from exc
        return data
    
    def create(self, validated_data):
        """Create user with hashed password"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
