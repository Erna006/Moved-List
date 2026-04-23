# Moved-List

# 🎬 CineHub — Movie Catalog Website

A full-stack web application for browsing, reviewing, and managing favorite movies.
Built with **Angular** (frontend) and **Django REST Framework** (backend).

---

## 👥 Group Members

| Name |
|------|
| Sarsemkhan Yernazar |
| Nurtaev Ospanali |
| Madi Adilet |

**Practice Lesson:** Thursday 10:00-12:00

---

## 📌 Project Description

CineHub is a movie catalog platform where users can:

- Browse and search movies by title, genre, country, language, and year
- View detailed movie pages with trailers, cast, and ratings
- Register and log in using JWT authentication
- Leave reviews and rate movies (1–10 scale)
- Save movies to a personal favorites list

---

## ✅ Requirements Coverage

### Frontend (Angular)
| Requirement | Status |
|-------------|--------|
| Interfaces & services for API | ✅ |
| 4+ click events triggering API requests | ✅ (search, add to favorites, submit review, logout) |
| 4+ form controls with [(ngModel)] | ✅ (login, register, search, review rating & comment) |
| Basic CSS styling | ✅ |
| Routing with 3+ named routes | ✅ (/films, /films/:id, /login, /register, /favorites) |
| @for / @if (or *ngFor / *ngIf) | ✅ |
| JWT authentication + interceptor + logout | ✅ |
| Angular Service with HttpClient | ✅ (FilmService, AuthService, ReviewService, etc.) |
| API error handling | ✅ |

### Backend (Django + DRF)
| Requirement | Status |
|-------------|--------|
| 4+ models | ✅ (Film, Genre, Review, Favorite, Actor, Country, Language) |
| Custom model manager | ✅ (FilmManager) |
| 2+ ForeignKey relationships | ✅ (Review→User, Review→Film, Favorite→User, Favorite→Film) |
| 2+ serializers.Serializer | ✅ (FilmSearchSerializer, UserStatsSerializer) |
| 2+ serializers.ModelSerializer | ✅ (FilmDetailSerializer, ReviewSerializer, etc.) |
| 2+ FBV with DRF decorators | ✅ (film_list_simple, site_stats) |
| 2+ CBV using APIView | ✅ (UserProfileView, LogoutView) |
| Token-based auth (login + logout) | ✅ |
| Full CRUD for at least 1 model | ✅ (Review: create, read, update, delete) |
| Objects linked to request.user | ✅ (Review, Favorite) |
| CORS configured | ✅ |
| Postman collection | ✅ (see /postman folder) |
