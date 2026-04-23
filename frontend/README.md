# 🎬 MovieList — Movie Catalog Website

A full-stack web application for browsing, reviewing, and managing favorite movies.
Built with **Angular** (frontend) and **Django REST Framework** (backend).

---

## 👥 Group Members

| Name | Role |
|------|------|
| Sarsemkhan Yernazar | Full-stack Developer |
| Nurtaev Ospanali | Full-stack Developer |
| Madi Adilet | Full-stack Developer |

**Practice Lesson:** Thursday 10:00-12:00

---

## 📌 Project Description

MovieList is a movie catalog platform where users can:

- Browse and search movies by title, genre, country, language, and year
- View detailed movie pages with cast, reviews and ratings
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

---

## 🚀 Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create_test_data
python manage.py runserver
```

Backend runs at: `http://127.0.0.1:8000`

### Frontend

```bash
cd frontend
npm install
ng serve
```

Frontend runs at: `http://localhost:4200`

---

## 📁 Project Structure