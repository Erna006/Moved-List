from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (
    Film, Genre, Country, Language, Actor, 
    Review, Favorite
)

from .serializers import (
    FilmListSerializer, FilmDetailSerializer,
    GenreSerializer, CountrySerializer, LanguageSerializer,
    ActorSerializer, ReviewSerializer, FavoriteSerializer,
    UserSerializer, UserRegistrationSerializer, LoginSerializer, LogoutSerializer
)

from .filters import FilmFilter

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'ok', 'service': 'movies-api'})


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info(request):
    return Response({
        'name': 'Movies API',
        'version': '1.0',
        'auth': ['jwt login', 'jwt refresh', 'jwt logout']
    })


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        token_serializer = TokenObtainPairSerializer(data=serializer.validated_data)
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data.get('refresh')
        if refresh:
            try:
                token = RefreshToken(refresh)
                token.blacklist()
            except Exception:
                pass

        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet to genre (only reading)"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
 
 
class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet to countries (only reading)"""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
 
 
class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet to languages (only reading)"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
 
 
class ActorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet to actors (only reading)"""
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
 
 
class FilmViewSet(viewsets.ModelViewSet):
    """
    ViewSet to films with full functionality:
    - Search by title
    - Filter by genre, country, language, year, rating
    - Ordering by rating, year, title
    """
    queryset = Film.objects.all().prefetch_related(
        'genres', 'countries', 'languages', 'actors', 'reviews'
    )
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    
    filterset_class = FilmFilter
    
    search_fields = ['title']
    
    ordering_fields = ['year', 'title', 'average_rating']
    ordering = ['-year']  
    def get_serializer_class(self):
        """Use different serializers for list and detail views"""
        if self.action == 'retrieve':
            return FilmDetailSerializer
        return FilmListSerializer
    
    def get_queryset(self):
        """
        Additional filtering for sorting by rating
        (since it's a calculated field)
        """
        queryset = super().get_queryset()
        
        ordering = self.request.query_params.get('ordering', '')
        if 'average_rating' in ordering:
            from django.db.models import Avg
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating')
            )
            if ordering == 'average_rating':
                queryset = queryset.order_by('avg_rating')
            elif ordering == '-average_rating':
                queryset = queryset.order_by('-avg_rating')
        
        return queryset
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_favorites(self, request, pk=None):
        """Add film to favorites"""
        film = self.get_object()
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            film=film
        )
        
        if created:
            return Response(
                {'message': 'Film added to favorites'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'Film already in favorites'},
                status=status.HTTP_200_OK
            )
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_from_favorites(self, request, pk=None):
        """Remove film from favorites"""
        film = self.get_object()
        deleted, _ = Favorite.objects.filter(
            user=request.user,
            film=film
        ).delete()
        
        if deleted:
            return Response(
                {'message': 'Film removed from favorites'},
                status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response(
                {'message': 'Film not found in favorites'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a film"""
        film = self.get_object()
        reviews = film.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
 
 
class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for reviews"""
    queryset = Review.objects.all().select_related('user', 'film')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['film', 'user']
    
    def perform_create(self, serializer):
        """Automatically set the user when creating a review"""
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        """User can only edit their own reviews"""
        queryset = super().get_queryset()
        if self.action in ['update', 'partial_update', 'destroy']:
            queryset = queryset.filter(user=self.request.user)
        return queryset
 
 
class FavoriteViewSet(viewsets.ModelViewSet):
    """ViewSet for favorite films"""
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Show only the current user's favorites"""
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('film').prefetch_related(
            'film__genres', 'film__countries'
        )
    
    def perform_create(self, serializer):
        """Automatically set the user"""
        serializer.save(user=self.request.user)
 
 
class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get information about the current user"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    'message': 'User successfully registered',
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)