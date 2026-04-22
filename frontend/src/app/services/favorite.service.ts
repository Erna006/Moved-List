import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Favorite } from '../models/film.model';

@Injectable({
  providedIn: 'root'
})
export class FavoriteService {
  private apiUrl = `${environment.apiUrl}/favorites/`;

  constructor(private http: HttpClient) { }

  /**
   * Получить список избранных фильмов
   */
  getFavorites(): Observable<Favorite[]> {
    return this.http.get<Favorite[]>(this.apiUrl);
  }

  /**
   * Добавить фильм в избранное
   */
  addToFavorites(filmId: number): Observable<Favorite> {
    return this.http.post<Favorite>(this.apiUrl, { film_id: filmId });
  }

  /**
   * Удалить из избранного
   */
  removeFromFavorites(favoriteId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${favoriteId}/`);
  }
}
