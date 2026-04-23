
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FavoriteService } from '../../services/favorite.service';
import { AuthService } from '../../services/auth.service';
import { Favorite } from '../../models/film.model';

@Component({
  selector: 'app-favorites',
  templateUrl: './favorites.component.html',
  styleUrls: ['./favorites.component.css']
})
export class FavoritesComponent implements OnInit {
  favorites: Favorite[] = [];
  loading = true;
  error = '';

  constructor(
    private favoriteService: FavoriteService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    if (!this.authService.isLoggedIn()) {
      this.router.navigate(['/login'], {
        queryParams: { returnUrl: '/favorites' }
      });
      return;
    }

    this.loadFavorites();
  }

  loadFavorites(): void {
    this.loading = true;
    this.error = '';

    this.favoriteService.getFavorites().subscribe({
      next: (favorites) => {
        this.favorites = favorites;
        this.loading = false;
      },
      error: () => {
        this.error = 'Failed to load favorites';
        this.loading = false;
      }
    });
  }

  removeFromFavorites(favorite: Favorite): void {
    if (confirm(`Remove "${favorite.film.title}" from favorites?`)) {
      this.favoriteService.removeFromFavorites(favorite.id).subscribe({
        next: () => {
          this.favorites = this.favorites.filter(f => f.id !== favorite.id);
        },
        error: () => {
          this.error = 'Failed to remove from favorites. Please try again.';
        }
      });
    }
  }
}
