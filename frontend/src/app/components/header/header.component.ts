// src/app/components/header/header.component.ts

import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {
  constructor(
    public authService: AuthService
  ) {}

  logout(): void {
    if (confirm('Вы уверены, что хотите выйти?')) {
      this.authService.logout();
    }
  }

  get currentUser() {
    return this.authService.currentUserValue;
  }

  get isLoggedIn() {
    return this.authService.isLoggedIn();
  }
}
