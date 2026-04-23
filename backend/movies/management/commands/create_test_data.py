from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from movies.models import Actor, Country, Film, FilmActor, Genre, Language, Review


class Command(BaseCommand):
    help = 'Creates test data for the movie website'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')

        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'is_staff': False,
                'is_superuser': False,
            },
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created user: testuser / testpass123'))

        genres_data = [
            ('Action', 'action'),
            ('Drama', 'drama'),
            ('Comedy', 'comedy'),
            ('Sci-Fi', 'sci-fi'),
            ('Thriller', 'thriller'),
            ('Detective', 'detective'),
            ('Adventure', 'adventure'),
            ('Horror', 'horror'),
            ('Romance', 'romance'),
            ('Fantasy', 'fantasy'),
        ]

        genres = {}
        for name, slug in genres_data:
            genre, _ = Genre.objects.get_or_create(
                slug=slug,
                defaults={'name': name},
            )
            genres[slug] = genre
        self.stdout.write(self.style.SUCCESS(f'Created {len(genres)} genres'))

        countries_data = [
            ('United States', 'USA'),
            ('United Kingdom', 'UK'),
            ('France', 'FR'),
            ('Germany', 'DE'),
            ('Russia', 'RU'),
            ('Japan', 'JP'),
            ('Italy', 'IT'),
            ('Spain', 'ES'),
            ('Canada', 'CA'),
            ('Australia', 'AU'),
        ]

        countries = {}
        for name, code in countries_data:
            country, _ = Country.objects.get_or_create(
                code=code,
                defaults={'name': name},
            )
            countries[code] = country
        self.stdout.write(self.style.SUCCESS(f'Created {len(countries)} countries'))

        languages_data = [
            ('English', 'en'),
            ('Russian', 'ru'),
            ('French', 'fr'),
            ('German', 'de'),
            ('Spanish', 'es'),
            ('Japanese', 'ja'),
            ('Italian', 'it'),
            ('Chinese', 'zh'),
        ]

        languages = {}
        for name, code in languages_data:
            language, _ = Language.objects.get_or_create(
                code=code,
                defaults={'name': name},
            )
            languages[code] = language
        self.stdout.write(self.style.SUCCESS(f'Created {len(languages)} languages'))

        actors_data = [
            'Leonardo DiCaprio',
            'Tom Hanks',
            'Scarlett Johansson',
            'Robert Downey Jr.',
            'Morgan Freeman',
            'Brad Pitt',
            'Johnny Depp',
            'Matt Damon',
            'Christian Bale',
            'Marion Cotillard',
            'Keanu Reeves',
            'Samuel L. Jackson',
            'Natalie Portman',
            'Tom Cruise',
            'Will Smith',
        ]

        actors = {}
        for name in actors_data:
            actor, _ = Actor.objects.get_or_create(
                name=name,
                defaults={'bio': f'Well-known actor {name}'},
            )
            actors[name] = actor
        self.stdout.write(self.style.SUCCESS(f'Created {len(actors)} actors'))

        films_data = [
            {
                'title': 'Inception',
                'description': 'A professional thief who steals information by infiltrating the subconscious of his targets during sleep gets a chance at redemption through one final mission: planting an idea instead of stealing one.',
                'year': 2010,
                'duration': 148,
                'genres': ['action', 'sci-fi', 'thriller'],
                'countries': ['USA', 'UK'],
                'languages': ['en', 'ru', 'fr'],
                'actors': ['Leonardo DiCaprio', 'Marion Cotillard', 'Tom Hanks'],
            },
            {
                'title': 'The Shawshank Redemption',
                'description': 'Banker Andy Dufresne is convicted of murdering his wife and her lover. In Shawshank prison, he faces cruelty and injustice on both sides of the bars.',
                'year': 1994,
                'duration': 142,
                'genres': ['drama'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Morgan Freeman', 'Tom Hanks'],
            },
            {
                'title': 'The Matrix',
                'description': 'Thomas Anderson leads a double life: by day he is an ordinary office worker, by night he becomes the hacker Neo and discovers there is no limit to how far the truth can reach.',
                'year': 1999,
                'duration': 136,
                'genres': ['action', 'sci-fi'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Keanu Reeves'],
            },
            {
                'title': 'The Dark Knight',
                'description': 'Batman raises the stakes in his war on crime. With Lieutenant Jim Gordon and District Attorney Harvey Dent, he sets out to rid Gotham of crime, but chaos soon takes over through the Joker.',
                'year': 2008,
                'duration': 152,
                'genres': ['action', 'thriller', 'detective'],
                'countries': ['USA', 'UK'],
                'languages': ['en', 'ru'],
                'actors': ['Christian Bale', 'Morgan Freeman'],
            },
            {
                'title': 'Forrest Gump',
                'description': 'Through the eyes of Forrest Gump, a kind-hearted man with a simple mind, we see the story of his extraordinary life.',
                'year': 1994,
                'duration': 142,
                'genres': ['drama', 'romance'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Tom Hanks'],
            },
            {
                'title': 'Interstellar',
                'description': 'When drought pushes humanity toward a food crisis, a team of explorers travels through a wormhole to find a planet suitable for human life.',
                'year': 2014,
                'duration': 169,
                'genres': ['sci-fi', 'drama', 'adventure'],
                'countries': ['USA', 'UK'],
                'languages': ['en', 'ru'],
                'actors': ['Matt Damon'],
            },
            {
                'title': 'The Avengers',
                'description': 'Loki returns, and this time he is not alone. Earth stands on the brink of invasion, and only a team of extraordinary heroes can save humanity.',
                'year': 2012,
                'duration': 143,
                'genres': ['action', 'sci-fi', 'fantasy'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Robert Downey Jr.', 'Scarlett Johansson', 'Samuel L. Jackson'],
            },
            {
                'title': 'Gladiator',
                'description': 'Maximus, a powerful Roman general and the emperor’s favorite, is betrayed by the new emperor Commodus and loses everything. He survives and becomes a gladiator.',
                'year': 2000,
                'duration': 155,
                'genres': ['action', 'drama', 'adventure'],
                'countries': ['USA', 'UK'],
                'languages': ['en', 'ru'],
                'actors': ['Tom Hanks'],
            },
            {
                'title': 'Pirates of the Caribbean',
                'description': 'The life of the charismatic adventurer Captain Jack Sparrow is full of surprises until his sworn enemy, Captain Barbossa, steals Jack’s ship, the Black Pearl.',
                'year': 2003,
                'duration': 143,
                'genres': ['adventure', 'fantasy', 'action'],
                'countries': ['USA'],
                'languages': ['en', 'ru'],
                'actors': ['Johnny Depp'],
            },
            {
                'title': 'Leon',
                'description': 'A professional hitman named Leon unexpectedly decides to help his 12-year-old neighbor Mathilda after her family is murdered by gangsters.',
                'year': 1994,
                'duration': 110,
                'genres': ['thriller', 'drama', 'detective'],
                'countries': ['FR'],
                'languages': ['en', 'fr', 'ru'],
                'actors': ['Natalie Portman'],
            },
        ]

        created_films = []
        for film_data in films_data:
            if Film.objects.filter(title=film_data['title']).exists():
                self.stdout.write(f'  Film "{film_data["title"]}" already exists')
                continue

            film = Film.objects.create(
                title=film_data['title'],
                description=film_data['description'],
                year=film_data['year'],
                duration=film_data['duration'],
            )

            for genre_slug in film_data['genres']:
                if genre_slug in genres:
                    film.genres.add(genres[genre_slug])

            for country_code in film_data['countries']:
                if country_code in countries:
                    film.countries.add(countries[country_code])

            for language_code in film_data['languages']:
                if language_code in languages:
                    film.languages.add(languages[language_code])

            for index, actor_name in enumerate(film_data['actors']):
                if actor_name in actors:
                    FilmActor.objects.create(
                        film=film,
                        actor=actors[actor_name],
                        order=index,
                    )

            created_films.append(film)
            self.stdout.write(self.style.SUCCESS(f'  Created film: {film.title} ({film.year})'))

        self.stdout.write(self.style.SUCCESS(f'\nCreated {len(created_films)} films'))

        if created_films and user:
            review_count = 0
            for film in created_films[:5]:
                Review.objects.get_or_create(
                    user=user,
                    film=film,
                    defaults={
                        'rating': 9,
                        'comment': f'Excellent movie! {film.title} left a strong impression.',
                    },
                )
                review_count += 1
            self.stdout.write(self.style.SUCCESS(f'Created {review_count} reviews'))

        self.stdout.write(self.style.SUCCESS('\nTest data created successfully.'))
        self.stdout.write(self.style.SUCCESS('\nUse these credentials to log in:'))
        self.stdout.write(self.style.SUCCESS('  Username: testuser'))
        self.stdout.write(self.style.SUCCESS('  Password: testpass123'))
