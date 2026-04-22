// src/app/components/register/register.component.ts

import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  loading = false;
  submitted = false;
  error = '';
  success = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    // Если уже авторизован, перенаправляем
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/']);
    }
  }

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group({
      username: ['', [
        Validators.required,
        Validators.minLength(3),
        Validators.maxLength(150)
      ]],
      email: ['', [
        Validators.required,
        Validators.email
      ]],
      password: ['', [
        Validators.required,
        Validators.minLength(8)
      ]],
      password_confirm: ['', Validators.required]
    }, {
      validators: this.passwordMatchValidator
    });
  }

  // Валидатор совпадения паролей
  passwordMatchValidator(form: FormGroup) {
    const password = form.get('password');
    const confirmPassword = form.get('password_confirm');
    
    if (password && confirmPassword && password.value !== confirmPassword.value) {
      confirmPassword.setErrors({ passwordMismatch: true });
      return { passwordMismatch: true };
    }
    return null;
  }

  // Удобный доступ к полям формы
  get f() {
    return this.registerForm.controls;
  }

  onSubmit(): void {
    this.submitted = true;
    this.error = '';
    this.success = false;

    // Останавливаемся, если форма невалидна
    if (this.registerForm.invalid) {
      return;
    }

    this.loading = true;

    this.authService.register(this.registerForm.value).subscribe({
      next: () => {
        this.success = true;
        this.loading = false;
        
        // Перенаправляем на страницу входа через 2 секунды
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (err: HttpErrorResponse) => {
        this.loading = false;
        
        if (err.error) {
          // Обрабатываем ошибки от сервера
          if (err.error.username) {
            this.error = 'Это имя пользователя уже занято';
          } else if (err.error.email) {
            this.error = 'Этот email уже используется';
          } else if (err.error.password) {
            this.error = err.error.password[0];
          } else {
            this.error = 'Ошибка регистрации. Проверьте введенные данные.';
          }
        } else {
          this.error = 'Произошла ошибка при регистрации. Попробуйте позже.';
        }
      }
    });
  }
}
