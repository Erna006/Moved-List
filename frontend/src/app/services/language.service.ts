import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { Language } from '../models/film.model';

@Injectable({
  providedIn: 'root'
})
export class LanguageService {
  private apiUrl = `${environment.apiUrl}/languages/`;

  constructor(private http: HttpClient) { }

  /**
   * Получить список всех языков
   */
  getLanguages(): Observable<Language[]> {
    return this.http.get<Language[]>(this.apiUrl);
  }
}
