from django.shortcuts import render 
from django.http import HttpResponse

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import urllib, base64
import numpy as np

from .models import Movie

# Create your views here.

def home(request):
    #return HttpResponse ('<h1>Welcome to home page</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Mariana Jaramillo Herrera'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies= Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})   


def about(request):
    return HttpResponse ('<h1>Welcome to about page</h1>')
    #return render(request, 'about.html', {'name':'Mariana Jaramillo Herrera'})

def signup_view(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

def statistics_view(request):
    all_movies = Movie.objects.all()

    # === Películas por año ===
    movie_counts_by_year = {}
    for movie in all_movies:
        year = str(movie.year) if movie.year else "Unknown"
        movie_counts_by_year[year] = movie_counts_by_year.get(year, 0) + 1

    # Ordenar años numéricamente (excepto "Unknown")
    sorted_years = sorted(
        [y for y in movie_counts_by_year.keys() if y != "Unknown"],
        key=lambda x: int(x)
    )
    if "Unknown" in movie_counts_by_year:
        sorted_years = ["Unknown"] + sorted_years
    sorted_counts = [movie_counts_by_year[y] for y in sorted_years]

    plt.figure(figsize=(9, 4))
    plt.bar(sorted_years, sorted_counts, color="#4A90E2", edgecolor='black', width=0.6)
    plt.title("Movies per year", fontsize=14, fontweight='bold', color="#333")
    plt.xlabel("Year", fontsize=11)
    plt.ylabel("Movies", fontsize=11)
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.tight_layout()

    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png', dpi=100, bbox_inches='tight')
    buffer1.seek(0)
    graphic_year = base64.b64encode(buffer1.getvalue()).decode('utf-8')
    buffer1.close()
    plt.close()

    # === Películas por primer género ===
    movie_counts_by_genre = {}
    for movie in all_movies:
        if movie.genre:
            # Tomar el primer género antes de "|" o ","
            first_genre = movie.genre.split('|')[0].split(',')[0].strip()
            movie_counts_by_genre[first_genre] = movie_counts_by_genre.get(first_genre, 0) + 1

    # Ordenar géneros por cantidad (de mayor a menor)
    sorted_genres = sorted(movie_counts_by_genre.items(), key=lambda x: x[1], reverse=True)
    genres = [g[0] for g in sorted_genres]
    counts = [g[1] for g in sorted_genres]

    # Gráfico horizontal para que se vean todos los géneros
    plt.figure(figsize=(9, len(genres) * 0.3))  # Altura dinámica según cantidad de géneros
    plt.barh(genres, counts, color="#50E3C2", edgecolor='black')
    plt.title("Movies per Genre (First Genre Only)", fontsize=14, fontweight='bold', color="#333")
    plt.xlabel("Movies", fontsize=11)
    plt.ylabel("Genre", fontsize=11)
    plt.gca().invert_yaxis()  # Para que el género más popular quede arriba
    plt.tight_layout()

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png', dpi=100, bbox_inches='tight')
    buffer2.seek(0)
    graphic_genre = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    buffer2.close()
    plt.close()

    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre,
    })
