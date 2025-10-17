from django.core.management.base import BaseCommand
from movie.models import Movie
import os
import json


class Command(BaseCommand):
    help = 'Load movies from movie_descriptions.json into the Movie model'

    def handle(self, *args, **kwargs):
        # Ruta del archivo JSON
        json_file_path = 'movie/management/commands/movies.json'

        # Cargar datos del archivo JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            movies = json.load(file)

        # Agregar películas a la base de datos
        for movie in movies:
            title = movie.get('movie_title', '').strip()
            genre = movie.get('genres', '')
            year = movie.get('title_year')
            description = movie.get('plot_keywords', '')

            exist = Movie.objects.filter(title=title).first()  # Evita duplicados
            if not exist:
                Movie.objects.create(
                    title=title,
                    image='movie/images/default.jpg',
                    genre=genre,
                    year=year if year else 0,
                    description=description
                )

        self.stdout.write(self.style.SUCCESS('Películas cargadas correctamente en la base de datos'))
