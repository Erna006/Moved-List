// src/app/components/film-detail/film-detail.component.ts

import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { FilmService } from '../../services/film.service';
import { ReviewService } from '../../services/review.service';
import { AuthService } from '../../services/auth.service';
import { Film, Review } from '../../models/film.model';

@Component({
  selector: 'app-film-detail',
  templateUrl: './film-detail.component.html',
  styleUrls: ['./film-detail.component.css']
})
export class FilmDetailComponent implements OnInit {
  film: Film | null = null;
  loading = true;
  error = '';
  actionError = '';
  
  // Отзывы
  reviewForm!: FormGroup;
  submittingReview = false;
  userReview: Review | null = null;
  editingReview = false;
  
  // Избранное
  isFavorite = false;
  favoriteLoading = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder,
    private filmService: FilmService,
    private reviewService: ReviewService,
    public authService: AuthService
  ) {}

  ngOnInit(): void {
    this.reviewForm = this.formBuilder.group({
      rating: [5, [Validators.required, Validators.min(1), Validators.max(10)]],
      comment: ['', [Validators.required, Validators.minLength(10)]]
    });

    const filmId = Number(this.route.snapshot.paramMap.get('id'));
    if (filmId) {
      this.loadFilm(filmId);
    } else {
      this.error = 'Неверный ID фильма';
      this.loading = false;
    }
  }

  loadFilm(id: number): void {
    this.loading = true;
    this.error = '';

    this.filmService.getFilm(id).subscribe({
      next: (film) => {
        this.film = film;
        this.loading = false;
        
        // Проверяем, есть ли отзыв от текущего пользователя
        if (this.authService.isLoggedIn() && film.reviews) {
          const currentUser = this.authService.currentUserValue;
          this.userReview = film.reviews.find(r => r.user.id === currentUser?.id) || null;
          
          if (this.userReview) {
            this.reviewForm.patchValue({
              rating: this.userReview.rating,
              comment: this.userReview.comment
            });
          }
        }
      },
      error: (err) => {
        this.error = 'Фильм не найден';
        this.loading = false;
      }
    });
  }

  // Управление избранным
  toggleFavorite(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login'], { 
        queryParams: { returnUrl: `/films/${this.film?.id}` } 
      });
      return;
    }

    if (!this.film) return;

    this.favoriteLoading = true;
    this.actionError = '';

    if (this.isFavorite) {
      // Удалить из избранного
      this.filmService.removeFromFavorites(this.film.id).subscribe({
        next: () => {
          this.isFavorite = false;
          this.favoriteLoading = false;
        },
        error: () => {
          this.favoriteLoading = false;
          this.actionError = 'Не удалось удалить фильм из избранного.';
        }
      });
    } else {
      // Добавить в избранное
      this.filmService.addToFavorites(this.film.id).subscribe({
        next: () => {
          this.isFavorite = true;
          this.favoriteLoading = false;
        },
        error: () => {
          this.favoriteLoading = false;
          this.actionError = 'Не удалось добавить фильм в избранное.';
        }
      });
    }
  }

  // Отправка отзыва
  submitReview(): void {
    if (this.reviewForm.invalid || !this.film) {
      return;
    }

    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login'], { 
        queryParams: { returnUrl: `/films/${this.film.id}` } 
      });
      return;
    }

    this.submittingReview = true;
    this.actionError = '';

    const reviewData = {
      film: this.film.id,
      rating: this.reviewForm.value.rating,
      comment: this.reviewForm.value.comment
    };

    if (this.userReview && this.editingReview) {
      // Обновление существующего отзыва
      this.reviewService.updateReview(this.userReview.id, {
        rating: reviewData.rating,
        comment: reviewData.comment
      }).subscribe({
        next: (review) => {
          this.userReview = review;
          this.editingReview = false;
          this.submittingReview = false;
          this.loadFilm(this.film!.id); // Перезагружаем фильм для обновления рейтинга
        },
        error: () => {
          this.submittingReview = false;
          this.actionError = 'Ошибка при обновлении отзыва.';
        }
      });
    } else {
      // Создание нового отзыва
      this.reviewService.createReview(reviewData).subscribe({
        next: (review) => {
          this.userReview = review;
          this.submittingReview = false;
          this.loadFilm(this.film!.id); // Перезагружаем фильм для обновления рейтинга
        },
        error: (err) => {
          this.submittingReview = false;
          if (err.status === 400) {
            this.actionError = 'Вы уже оставили отзыв на этот фильм.';
          } else {
            this.actionError = 'Ошибка при создании отзыва.';
          }
        }
      });
    }
  }

  // Редактирование отзыва
  startEditReview(): void {
    this.editingReview = true;
  }

  cancelEditReview(): void {
    this.editingReview = false;
    if (this.userReview) {
      this.reviewForm.patchValue({
        rating: this.userReview.rating,
        comment: this.userReview.comment
      });
    }
  }

  // Удаление отзыва
  deleteReview(): void {
    if (!this.userReview) return;

    if (confirm('Вы уверены, что хотите удалить свой отзыв?')) {
      this.reviewService.deleteReview(this.userReview.id).subscribe({
        next: () => {
          this.userReview = null;
          this.reviewForm.reset({ rating: 5, comment: '' });
          this.loadFilm(this.film!.id);
        },
        error: () => {
          this.actionError = 'Ошибка при удалении отзыва.';
        }
      });
    }
  }

  getStars(rating: number): boolean[] {
    return Array(10).fill(false).map((_, i) => i < rating);
  }

  goBack(): void {
    this.router.navigate(['/films']);
  }
}
