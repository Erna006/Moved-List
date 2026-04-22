import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FilmListComponent } from './components/film-list/film-list.component';
import { FilmDetailComponent } from './components/film-detail/film-detail.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { FavoritesComponent } from './components/favorites/favorites.component';

const routes: Routes = [
  { path: '', redirectTo: '/films', pathMatch: 'full' },
  { path: 'films', component: FilmListComponent },
  { path: 'films/:id', component: FilmDetailComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'favorites', component: FavoritesComponent },
  { path: '**', redirectTo: '/films' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
