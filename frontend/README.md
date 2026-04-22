# 🎬 Movie Frontend - Angular приложение

Фронтенд для сайта с фильмами на Angular.

## 🚀 Быстрый старт

### Установка зависимостей
```bash
npm install
```

### Запуск сервера разработки
```bash
ng serve
```

Приложение будет доступно по адресу: `http://localhost:4200`

### Сборка для продакшена
```bash
ng build --configuration production
```

## 📋 Требования

- Node.js 16+
- npm 8+
- Angular CLI 15+

## 🔧 Установка Angular CLI

```bash
npm install -g @angular/cli
```

## ⚙️ Настройка

### API URL

По умолчанию API URL указан как `http://127.0.0.1:8000/api`

Измените в файлах:
- `src/environments/environment.ts` - для разработки
- `src/environments/environment.prod.ts` - для продакшена

## 📁 Структура проекта

```
src/
├── app/
│   ├── components/       # Angular компоненты
│   │   ├── film-list/
│   │   ├── film-detail/
│   │   ├── login/
│   │   ├── register/
│   │   ├── header/
│   │   └── favorites/
│   ├── services/         # Сервисы для API
│   ├── models/           # TypeScript интерфейсы
│   ├── interceptors/     # HTTP interceptors
│   ├── app.component.*
│   ├── app.module.ts
│   └── app-routing.module.ts
├── environments/         # Конфигурация окружений
├── assets/              # Статические файлы
├── index.html
└── styles.css
```

## ✨ Функционал

- 🔍 Поиск фильмов
- 🎭 Фильтрация по жанрам, странам, языкам
- ⭐ Сортировка по рейтингу и году
- 👤 Регистрация и авторизация
- 💬 Отзывы на фильмы
- ⭐ Избранные фильмы
- 📱 Адаптивный дизайн

## 🔐 Авторизация

Приложение использует JWT токены для авторизации.
Токены автоматически обновляются через HTTP interceptor.

## 📝 Доступные команды

- `npm start` - запуск dev сервера
- `npm run build` - production сборка
- `npm run watch` - сборка с watch mode
- `npm test` - запуск тестов

## 🌐 Backend

Для работы фронтенда требуется запущенный Django backend на `http://127.0.0.1:8000`

## 📄 Лицензия

MIT
