"""
Django management command для создания тестовых данных
Расположение: backend/movies/management/commands/create_test_data.py
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from movies.models import Genre, Country, Language, Actor, Film, FilmActor, Review


class Command(BaseCommand):
    help = 'Создает тестовые данные для сайта с фильмами'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')

        # Создаем тестового пользователя
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'is_staff': False,
                'is_superuser': False
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('✓ Создан пользователь: testuser / testpass123'))

        # Создаем жанры
        genres_data = [
            ('Боевик', 'action'),
            ('Драма', 'drama'),
            ('Комедия', 'comedy'),
            ('Фантастика', 'sci-fi'),
            ('Триллер', 'thriller'),
            ('Детектив', 'detective'),
            ('Приключения', 'adventure'),
            ('Ужасы', 'horror'),
            ('Мелодрама', 'romance'),
            ('Фэнтези', 'fantasy'),
        ]
        
        genres = {}
        for name, slug in genres_data:
            genre, created = Genre.objects.get_or_create(
                slug=slug,
                defaults={'name': name}
            )
            genres[slug] = genre
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(genres)} жанров'))

        # Создаем страны
        countries_data = [
            ('США', 'USA'),
            ('Великобритания', 'UK'),
            ('Франция', 'FR'),
            ('Германия', 'DE'),
            ('Россия', 'RU'),
            ('Япония', 'JP'),
            ('Италия', 'IT'),
            ('Испания', 'ES'),
            ('Канада', 'CA'),
            ('Австралия', 'AU'),
        ]
        
        countries = {}
        for name, code in countries_data:
            country, created = Country.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            countries[code] = country
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(countries)} стран'))

        # Создаем языки
        languages_data = [
            ('Английский', 'en'),
            ('Русский', 'ru'),
            ('Французский', 'fr'),
            ('Немецкий', 'de'),
            ('Испанский', 'es'),
            ('Японский', 'ja'),
            ('Итальянский', 'it'),
            ('Китайский', 'zh'),
        ]
        
        languages = {}
        for name, code in languages_data:
            language, created = Language.objects.get_or_create(
                code=code,
                defaults={'name': name}
            )
            languages[code] = language
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(languages)} языков'))

        # Создаем актёров
        actors_data = [
            'Леонардо ДиКаприо',
            'Том Хэнкс',
            'Скарлетт Йоханссон',
            'Роберт Дауни мл.',
            'Морган Фриман',
            'Брэд Питт',
            'Джонни Депп',
            'Мэтт Дэймон',
            'Кристиан Бэйл',
            'Марион Котийяр',
            'Киану Ривз',
            'Сэмюэл Л. Джексон',
            'Натали Портман',
            'Том Круз',
            'Уилл Смит',
        ]
        
        actors = {}
        for name in actors_data:
            actor, created = Actor.objects.get_or_create(
                name=name,
                defaults={'bio': f'Известный актёр {name}'}
            )
            actors[name] = actor
        self.stdout.write(self.style.SUCCESS(f'✓ Создано {len(actors)} актёров'))

        # Создаем тестовые фильмы
        films_data = [
            {
                'title': 'Начало',
                'description': 'Профессиональный вор, который крадет информацию, проникая в подсознание жертв во время сна, получает шанс на искупление. Для этого ему предстоит выполнить невозможное: он должен не украсть идею, а внедрить ее в сознание человека.',
                'year': 2010,
                'duration': 148,
                'genres': ['action', 'sci-fi', 'thriller'],
                'countries': ['USA', 'UK'],
                'languages': ['en', 'ru', 'fr'],
                'actors': ['Леонардо ДиКаприо', 'Марион Котийяр', 'Том Хэнкс'],
            },
            {
                'title': 'Побег из Шоушенка',
                'description': 'Успешный банкир Энди Дюфрейн обвинен в убийстве собственной жены и ее любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решетки.',
                'year': 1994,
                'duration': 142,
                'genres': ['drama'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Морган Фриман', 'Том Хэнкс'],
            },
            {
                'title': 'Матрица',
                'description': 'Жизнь Томаса Андерсона разделена на две части: днём он — самый обычный офисный работник, получающий нагоняи от начальства, а ночью превращается в хакера по имени Нео, и нет места в сети, куда он не смог бы дотянуться.',
                'year': 1999,
                'duration': 136,
                'genres': ['action', 'sci-fi'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Киану Ривз'],
            },
            {
                'title': 'Тёмный рыцарь',
                'description': 'Бэтмен поднимает ставки в войне с криминалом. С помощью лейтенанта Джима Гордона и прокурора Харви Дента он намерен очистить улицы Готэма от преступности. Сотрудничество оказывается эффективным, но скоро они обнаруживают себя посреди хаоса, развязанного восходящим криминальным гением, известным напуганным горожанам под именем Джокер.',
                'year': 2008,
                'duration': 152,
                'genres': ['action', 'thriller', 'detective'],
                'countries': ['USA', 'UK'],
                'languages': ['en', 'ru'],
                'actors': ['Кристиан Бэйл', 'Морган Фриман'],
            },
            {
                'title': 'Форрест Гамп',
                'description': 'От лица главного героя Форреста Гампа, слабоумного безобидного человека с благородным и открытым сердцем, рассказывается история его необыкновенной жизни.',
                'year': 1994,
                'duration': 142,
                'genres': ['drama', 'romance'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Том Хэнкс'],
            },
            {
                'title': 'Интерстеллар',
                'description': 'Когда засуха приводит человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями.',
                'year': 2014,
                'duration': 169,
                'genres': ['sci-fi', 'drama', 'adventure'],
                'countries': ['USA', 'UK'],
                'languages': ['en', 'ru'],
                'actors': ['Мэтт Дэймон'],
            },
            {
                'title': 'Мстители',
                'description': 'Локи, сводный брат Тора, возвращается, и на этот раз он не один. Земля на грани порабощения, и только лучшие из лучших могут спасти человечество. Глава международной организации Щ.И.Т. Ник Фьюри собирает выдающихся поборников справедливости и добра, чтобы отразить атаку.',
                'year': 2012,
                'duration': 143,
                'genres': ['action', 'sci-fi', 'fantasy'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Роберт Дауни мл.', 'Скарлетт Йоханссон', 'Сэмюэл Л. Джексон'],
            },
            {
                'title': 'Гладиатор',
                'description': 'Максимус — могучий римский полководец, любимец императора. Однако, новый император — Коммод — приказывает уничтожить Максимуса и его семью. Чудом избежав гибели, Максимус становится гладиатором.',
                'year': 2000,
                'duration': 155,
                'genres': ['action', 'drama', 'adventure'],
                'countries': ['USA', 'UK'],
                'languages': ['en', 'ru'],
                'actors': ['Том Хэнкс'],
            },
            {
                'title': 'Пираты Карибского моря',
                'description': 'Жизнь харизматичного авантюриста капитана Джека Воробья полна приключений, пока его заклятый враг, капитан Барбосса, не похищает корабль Джека, Чёрную жемчужину.',
                'year': 2003,
                'duration': 143,
                'genres': ['adventure', 'fantasy', 'action'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Джонни Депп'],
            },
            {
                'title': 'Леон',
                'description': 'Профессиональный убийца Леон неожиданно для себя самого решает помочь 12-летней соседке Матильде, семью которой расстреляли бандиты.',
                'year': 1994,
                'duration': 110,
                'genres': ['thriller', 'drama', 'detective'],
                'countries': ['FR'],
                'languages': ['en', 'fr', 'ru'],
                'actors': ['Натали Портман'],
            },
        ]

        created_films = []
        for film_data in films_data:
            # Проверяем, существует ли уже фильм
            if Film.objects.filter(title=film_data['title']).exists():
                self.stdout.write(f'  Фильм "{film_data["title"]}" уже существует')
                continue

            # Создаем фильм
            film = Film.objects.create(
                title=film_data['title'],
                description=film_data['description'],
                year=film_data['year'],
                duration=film_data['duration'],
            )

            # Добавляем жанры
            for genre_slug in film_data['genres']:
                if genre_slug in genres:
                    film.genres.add(genres[genre_slug])

            # Добавляем страны
            for country_code in film_data['countries']:
                if country_code in countries:
                    film.countries.add(countries[country_code])

            # Добавляем языки
            for language_code in film_data['languages']:
                if language_code in languages:
                    film.languages.add(languages[language_code])

            # Добавляем актёров
            for i, actor_name in enumerate(film_data['actors']):
                if actor_name in actors:
                    FilmActor.objects.create(
                        film=film,
                        actor=actors[actor_name],
                        order=i
                    )

            created_films.append(film)
            self.stdout.write(self.style.SUCCESS(f'  ✓ Создан фильм: {film.title} ({film.year})'))

        self.stdout.write(self.style.SUCCESS(f'\n✓ Создано {len(created_films)} фильмов'))

        # Создаем тестовые отзывы
        if created_films and user:
            review_count = 0
            for film in created_films[:5]:  # Отзывы на первые 5 фильмов
                Review.objects.get_or_create(
                    user=user,
                    film=film,
                    defaults={
                        'rating': 9,
                        'comment': f'Отличный фильм! {film.title} оставил яркие впечатления.'
                    }
                )
                review_count += 1
            self.stdout.write(self.style.SUCCESS(f'✓ Создано {review_count} отзывов'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Тестовые данные успешно созданы!'))
        self.stdout.write(self.style.SUCCESS('\nДля входа используйте:'))
        self.stdout.write(self.style.SUCCESS('  Username: testuser'))
        self.stdout.write(self.style.SUCCESS('  Password: testpass123'))