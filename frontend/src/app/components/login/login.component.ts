// src/app/components/login/login.component.ts

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm!: FormGroup;
  loading = false;
  submitted = false;
  error = '';
  returnUrl = '';

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    // Если уже авторизован, перенаправляем
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/']);
    }
  }

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });

    // Получаем URL для возврата после входа
    this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/films';
  }

  // Удобный доступ к полям формы
  get f() {
    return this.loginForm.controls;
  }

  onSubmit(): void {
    this.submitted = true;
    this.error = '';

    // Останавливаемся, если форма невалидна
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;

    this.authService.login(this.loginForm.value).subscribe({
      next: () => {
        this.router.navigate([this.returnUrl]);
      },
      error: (err: HttpErrorResponse) => {
        if (err.status === 401) {
          this.error = 'Неверное имя пользователя или пароль';
        } else {
          this.error = 'Произошла ошибка при входе. Попробуйте позже.';
        }
        this.loading = false;
      }
    });
  }
}
