from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    FilmViewSet, GenreViewSet, CountryViewSet,
    LanguageViewSet, ActorViewSet, ReviewViewSet,
    FavoriteViewSet, UserViewSet, health_check,
    api_info, LoginAPIView, LogoutAPIView, RegisterAPIView
)

router = DefaultRouter()
router.register(r'films', FilmViewSet, basename='film')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'actors', ActorViewSet, basename='actor')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health_check'),
    path('info/', api_info, name='api_info'),
    path('auth/login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutAPIView.as_view(), name='token_logout'),
    path('auth/register/', RegisterAPIView.as_view(), name='user_register'),
]
