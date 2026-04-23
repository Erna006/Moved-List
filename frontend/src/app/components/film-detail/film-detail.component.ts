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

  reviewForm!: FormGroup;
  submittingReview = false;
  userReview: Review | null = null;
  editingReview = false;

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
      this.error = 'Invalid film ID';
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
      error: () => {
        this.error = 'Film not found';
        this.loading = false;
      }
    });
  }

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
      this.filmService.removeFromFavorites(this.film.id).subscribe({
        next: () => {
          this.isFavorite = false;
          this.favoriteLoading = false;
        },
        error: () => {
          this.favoriteLoading = false;
          this.actionError = 'Failed to remove the film from favorites.';
        }
      });
    } else {
      this.filmService.addToFavorites(this.film.id).subscribe({
        next: () => {
          this.isFavorite = true;
          this.favoriteLoading = false;
        },
        error: () => {
          this.favoriteLoading = false;
          this.actionError = 'Failed to add the film to favorites.';
        }
      });
    }
  }

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
      this.reviewService.updateReview(this.userReview.id, {
        rating: reviewData.rating,
        comment: reviewData.comment
      }).subscribe({
        next: (review) => {
          this.userReview = review;
          this.editingReview = false;
          this.submittingReview = false;
          this.loadFilm(this.film!.id);
        },
        error: () => {
          this.submittingReview = false;
          this.actionError = 'Failed to update the review.';
        }
      });
    } else {
      this.reviewService.createReview(reviewData).subscribe({
        next: (review) => {
          this.userReview = review;
          this.submittingReview = false;
          this.loadFilm(this.film!.id);
        },
        error: (err) => {
          this.submittingReview = false;
          if (err.status === 400) {
            this.actionError = 'You have already left a review for this film.';
          } else {
            this.actionError = 'Failed to create the review.';
          }
        }
      });
    }
  }

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

  deleteReview(): void {
    if (!this.userReview) return;

    if (confirm('Are you sure you want to delete your review?')) {
      this.reviewService.deleteReview(this.userReview.id).subscribe({
        next: () => {
          this.userReview = null;
          this.reviewForm.reset({ rating: 5, comment: '' });
          this.loadFilm(this.film!.id);
        },
        error: () => {
          this.actionError = 'Failed to delete the review.';
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
