// src/app/components/film-list/film-list.component.ts

import { Component, OnInit } from '@angular/core';
import { FilmService } from '../../services/film.service';
import { Film, FilmFilters, Genre, Country, Language } from '../../models/film.model';
import { GenreService } from '../../services/genre.service';
import { CountryService } from '../../services/country.service';
import { LanguageService } from '../../services/language.service';

@Component({
  selector: 'app-film-list',
  templateUrl: './film-list.component.html',
  styleUrls: ['./film-list.component.css']
})
export class FilmListComponent implements OnInit {
  films: Film[] = [];
  genres: Genre[] = [];
  countries: Country[] = [];
  languages: Language[] = [];

  // Фильтры
  filters: FilmFilters = {
    page: 1
  };

  // Состояние загрузки
  loading = false;
  error = '';

  // Пагинация
  totalCount = 0;
  currentPage = 1;
  pageSize = 20;

  onHover(film: any): void {
    film.showTrailer = true;
  }

  onLeave(film: any): void {
    film.showTrailer = false;
  }

  // Опции сортировки
  sortOptions = [
    { value: '-year', label: 'Year (newest first)' },
    { value: 'year', label: 'Year (oldest first)' },
    { value: 'title', label: 'Title (A-Z)' },
    { value: '-title', label: 'Title (Z-A)' },
    { value: '-average_rating', label: 'Rating (highest)' },
    { value: 'average_rating', label: 'Rating (lowest)' }
  ];

  constructor(
    private filmService: FilmService,
    private genreService: GenreService,
    private countryService: CountryService,
    private languageService: LanguageService
  ) { }

  ngOnInit(): void {
    this.loadFilters();
    this.loadFilms();
  }

  /**
   * Загрузить опции для фильтров
   */
  loadFilters(): void {
    this.genreService.getGenres().subscribe({
      next: (genres) => this.genres = genres,
      error: () => {
        this.error = 'Not able to load filters. Try to refresh the page.';
      }
    });

    this.countryService.getCountries().subscribe({
      next: (countries) => this.countries = countries,
      error: () => {
        this.error = 'Not able to load filters. Try to refresh the page.';
      }
    });

    this.languageService.getLanguages().subscribe({
      next: (languages) => this.languages = languages,
      error: () => {
        this.error = 'Not able to load filters. Try to refresh the page.';
      }
    });
  }

  /**
   * Загрузить фильмы с учетом фильтров
   */
  loadFilms(): void {
    this.loading = true;
    this.error = '';

    this.filmService.getFilms(this.filters).subscribe({
      next: (response: any) => {
        // Проверка на массив (ваш текущий случай)
        if (Array.isArray(response)) {
          this.films = response;
          this.totalCount = response.length;
        }
        // Проверка на объект с ключом results (стандарт DRF с пагинацией)
        else if (response && response.results) {
          this.films = response.results;
          this.totalCount = response.count;
        }
        else {
          this.films = [];
          this.totalCount = 0;
        }

        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.films = [];
        this.totalCount = 0;
        this.error = 'Not able to load films. Check your connection and try again.';
      }
    });
  }

  /**
   * Apply filters
   */
  applyFilters(): void {
    this.filters.page = 1; // Reset to first page
    this.currentPage = 1;
    this.loadFilms();
  }

  /**
   * Reset all filters
   */
  resetFilters(): void {
    this.filters = { page: 1 };
    this.currentPage = 1;
    this.loadFilms();
  }

  /**
   * Search by title
   */
  onSearchChange(searchTerm: string): void {
    this.filters.search = searchTerm || undefined;
    this.applyFilters();
  }

  /**
   * Change sorting
   */
  onSortChange(ordering: string): void {
    this.filters.ordering = ordering;
    this.applyFilters();
  }

  /**
   * Pagination - go to page
   */
  onPageChange(page: number): void {
    this.currentPage = page;
    this.filters.page = page;
    this.loadFilms();
    window.scrollTo(0, 0);
  }

  /**
   * Get array of pages for pagination
   */
  getPages(): number[] {
    const totalPages = Math.ceil(this.totalCount / this.pageSize);
    return Array.from({ length: totalPages }, (_, i) => i + 1);
  }
}
