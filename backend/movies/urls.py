from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import (
    FilmViewSet, GenreViewSet, CountryViewSet,
    LanguageViewSet, ActorViewSet, ReviewViewSet,
    FavoriteViewSet, UserViewSet, health_check,
    api_info, LoginAPIView, LogoutAPIView
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
    # API endpoints
    path('', include(router.urls)),
    path('health/', health_check, name='health_check'),
    path('info/', api_info, name='api_info'),
    
    # JWT Authentication
    path('auth/login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', LogoutAPIView.as_view(), name='token_logout'),
    path('auth/register/', UserViewSet.as_view({'post': 'register'}), name='user_register'),
]

"""
Доступные endpoints:

ФИЛЬМЫ:
GET    /api/films/                    - Список всех фильмов
GET    /api/films/{id}/               - Детали фильма
POST   /api/films/                    - Создать фильм (требует авторизации)
PUT    /api/films/{id}/               - Обновить фильм (требует авторизации)
DELETE /api/films/{id}/               - Удалить фильм (требует авторизации)
GET    /api/films/{id}/reviews/       - Отзывы на фильм
POST   /api/films/{id}/add_to_favorites/    - Добавить в избранное
DELETE /api/films/{id}/remove_from_favorites/ - Удалить из избранного

Параметры фильтрации для /api/films/:
- search=название                     - Поиск по названию (частичное совпадение)
- genre=1                             - Фильтр по жанру (ID)
- genres=1,2,3                        - Фильтр по нескольким жанрам
- country=1                           - Фильтр по стране (ID)
- countries=1,2                       - Фильтр по нескольким странам
- language=1                          - Фильтр по языку (ID)
- languages=1,2                       - Фильтр по нескольким языкам
- year=2023                           - Фильтр по году (точное совпадение)
- year_min=2020                       - Фильмы с года
- year_max=2024                       - Фильмы до года
- min_rating=7                        - Минимальный рейтинг
- ordering=year                       - Сортировка по году (возрастание)
- ordering=-year                      - Сортировка по году (убывание)
- ordering=title                      - Сортировка по названию
- ordering=-average_rating            - Сортировка по рейтингу (убывание)

ЖАНРЫ:
GET    /api/genres/                   - Список жанров
GET    /api/genres/{slug}/            - Детали жанра

СТРАНЫ:
GET    /api/countries/                - Список стран
GET    /api/countries/{id}/           - Детали страны

ЯЗЫКИ:
GET    /api/languages/                - Список языков
GET    /api/languages/{id}/           - Детали языка

АКТЁРЫ:
GET    /api/actors/                   - Список актёров
GET    /api/actors/{id}/              - Детали актёра
GET    /api/actors/?search=имя        - Поиск актёров

ОТЗЫВЫ:
GET    /api/reviews/                  - Список всех отзывов
GET    /api/reviews/{id}/             - Детали отзыва
POST   /api/reviews/                  - Создать отзыв (требует авторизации)
PUT    /api/reviews/{id}/             - Обновить отзыв (только свой)
DELETE /api/reviews/{id}/             - Удалить отзыв (только свой)
GET    /api/reviews/?film=1           - Отзывы на конкретный фильм

ИЗБРАННОЕ:
GET    /api/favorites/                - Избранные фильмы (требует авторизации)
POST   /api/favorites/                - Добавить в избранное
DELETE /api/favorites/{id}/           - Удалить из избранного

ПОЛЬЗОВАТЕЛИ:
GET    /api/users/me/                 - Информация о текущем пользователе
POST   /api/auth/register/            - Регистрация нового пользователя
POST   /api/auth/login/               - Получить JWT токен
POST   /api/auth/refresh/             - Обновить JWT токен

Примеры запросов:

1. Получить все боевики 2023 года с рейтингом от 7:
   GET /api/films/?genre=1&year=2023&min_rating=7

2. Поиск фильмов по названию:
   GET /api/films/?search=Матрица

3. Фильмы из США или Великобритании, отсортированные по рейтингу:
   GET /api/films/?countries=1,2&ordering=-average_rating

4. Фильмы 2020-2024 года на русском языке:
   GET /api/films/?year_min=2020&year_max=2024&language=1
"""