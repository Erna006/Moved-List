
export interface Genre {
  id: number;
  name: string;
  slug: string;
}

export interface Country {
  id: number;
  name: string;
  code: string;
}

export interface Language {
  id: number;
  name: string;
  code: string;
}

export interface Actor {
  id: number;
  name: string;
  photo?: string;
  bio?: string;
}

export interface FilmActor {
  actor: Actor;
  role?: string;
  order: number;
}

export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Review {
  id: number;
  user: User;
  film: number;
  rating: number;
  comment: string;
  created_at: string;
  updated_at: string;
}

export interface Film {
  id: number;
  title: string;
  description: string;
  year: number;
  duration: number;
  poster: string;
  genres: Genre[];
  countries: Country[];
  languages?: Language[];
  film_actors?: FilmActor[];
  reviews?: Review[];
  average_rating: number;
  reviews_count: number;
  created_at?: string;
  updated_at?: string;
  trailer_url?: string;
  showTrailer?: boolean;
}

export interface FilmListResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Film[];
}

export interface Favorite {
  id: number;
  film: Film;
  added_at: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface UserRegistration {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface FilmFilters {
  search?: string;
  genre?: number;
  genres?: number[];
  country?: number;
  countries?: number[];
  language?: number;
  languages?: number[];
  year?: number;
  year_min?: number;
  year_max?: number;
  min_rating?: number;
  ordering?: string;
  page?: number;
}
