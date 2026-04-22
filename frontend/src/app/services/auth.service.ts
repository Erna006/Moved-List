// src/app/services/auth.service.ts

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { AuthTokens, User, UserLogin, UserRegistration } from '../models/film.model';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private currentUserSubject: BehaviorSubject<User | null>;

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.currentUserSubject = new BehaviorSubject<User | null>(
      this.getUserFromStorage()
    );
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  /**
   * Регистрация нового пользователя
   */
  register(userData: UserRegistration): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register/`, userData);
  }

  /**
   * Вход в систему
   */
  login(credentials: UserLogin): Observable<AuthTokens> {
    return this.http.post<AuthTokens>(`${this.apiUrl}/auth/login/`, credentials)
      .pipe(
        tap(tokens => {
          this.saveTokens(tokens);
          this.getCurrentUser().subscribe();
        })
      );
  }

  /**
   * Выход из системы
   */
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('current_user');
    this.currentUserSubject.next(null);
    this.router.navigate(['/login']);
  }

  /**
   * Получить информацию о текущем пользователе
   */
  getCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/users/me/`)
      .pipe(
        tap(user => {
          localStorage.setItem('current_user', JSON.stringify(user));
          this.currentUserSubject.next(user);
        })
      );
  }

  /**
   * Обновить access token используя refresh token
   */
  refreshToken(): Observable<any> {
    const refreshToken = this.getRefreshToken();
    return this.http.post<{ access: string }>(`${this.apiUrl}/auth/refresh/`, {
      refresh: refreshToken
    }).pipe(
      tap(response => {
        localStorage.setItem('access_token', response.access);
      })
    );
  }

  /**
   * Сохранить токены в localStorage
   */
  private saveTokens(tokens: AuthTokens): void {
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
  }

  /**
   * Получить access token
   */
  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  /**
   * Получить refresh token
   */
  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  /**
   * Проверить, авторизован ли пользователь
   */
  isLoggedIn(): boolean {
    return !!this.getAccessToken();
  }

  /**
   * Получить пользователя из localStorage
   */
  private getUserFromStorage(): User | null {
    const userStr = localStorage.getItem('current_user');
    return userStr ? JSON.parse(userStr) : null;
  }
}
