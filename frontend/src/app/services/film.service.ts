import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Film, FilmListResponse, FilmFilters } from '../models/film.model';

@Injectable({
  providedIn: 'root'
})
export class FilmService {
  private apiUrl = `${environment.apiUrl}/films/`;

  constructor(private http: HttpClient) { }

  getFilms(filters?: FilmFilters): Observable<FilmListResponse> {
    let params = new HttpParams();

    if (filters) {
      if (filters.search) {
        params = params.set('search', filters.search);
      }
      if (filters.genre) {
        params = params.set('genre', filters.genre.toString());
      }
      if (filters.genres && filters.genres.length > 0) {
        params = params.set('genres', filters.genres.join(','));
      }
      if (filters.country) {
        params = params.set('country', filters.country.toString());
      }
      if (filters.countries && filters.countries.length > 0) {
        params = params.set('countries', filters.countries.join(','));
      }
      if (filters.language) {
        params = params.set('language', filters.language.toString());
      }
      if (filters.languages && filters.languages.length > 0) {
        params = params.set('languages', filters.languages.join(','));
      }
      if (filters.year) {
        params = params.set('year', filters.year.toString());
      }
      if (filters.year_min) {
        params = params.set('year_min', filters.year_min.toString());
      }
      if (filters.year_max) {
        params = params.set('year_max', filters.year_max.toString());
      }
      if (filters.min_rating) {
        params = params.set('min_rating', filters.min_rating.toString());
      }
      if (filters.ordering) {
        params = params.set('ordering', filters.ordering);
      }
      if (filters.page) {
        params = params.set('page', filters.page.toString());
      }
    }

    return this.http.get<FilmListResponse>(this.apiUrl, { params });
  }

  getFilm(id: number): Observable<Film> {
    return this.http.get<Film>(`${this.apiUrl}${id}/`);
  }

  addToFavorites(filmId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${filmId}/add_to_favorites/`, {});
  }

  removeFromFavorites(filmId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}${filmId}/remove_from_favorites/`);
  }
}
