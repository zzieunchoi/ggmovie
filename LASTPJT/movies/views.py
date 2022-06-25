from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Movie, MovieComment, Genre
from .forms import MovieCommentForm
from django.http import JsonResponse
from django.core.management import call_command
from community.models import Community
import random
# Create your views here.

movies_fixture = 'movies/fixtures/movies.json'
genres_fixture = 'movies/fixtures/genres.json'

@require_safe
def home(request):
    movies = Movie.objects.order_by('-vote_average')
    communities = Community.objects.order_by('-pk')
    context = {
        'movies': movies[:3],
        'communities': communities[:3]
    }
    return render(request, 'movies/home.html', context)


@require_GET
def index(request):
    movies = Movie.objects.all()
    if not movies:
        call_command('loaddata', genres_fixture, app_label='movies')
        call_command('loaddata', movies_fixture, app_label='movies')
        movies = Movie.objects.all()

    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    # movie = get_object_or_404(Movie, pk=movie_pk)
    movie = Movie.objects.get(pk= movie_pk)
    comment_form = MovieCommentForm()
    comments = movie.moviecomment_set.all()
    context = {
        'movie': movie,
        'comment_form':comment_form,
        'comments':comments,
    }
    return render(request, 'movies/detail.html', context)


@require_safe
def recommend(request, movie_pk):
    movie = get_object_or_404(Movie, pk = movie_pk)
    genres_list = movie.genres.filter(movie=movie_pk)
    movies = Movie.objects.all()
    comments = MovieComment.objects.filter(user = request.user).values('title')
    comments_list = []
    for c in comments:
        if c['title'] not in comments_list:
            comments_list.append(c['title'])
    movies_list = []
    for movie_data in movies:
        data_genres = movie_data.genres.filter(movie=movie_data.pk)
        if movie_data.pk != movie_pk:
            if movie_data.pk not in comments_list:
                for genre in genres_list:
                    if genre in data_genres:
                        if movie_data not in movies_list:
                            movies_list.append(movie_data)

    sorted(movies_list, key=lambda k:k.vote_average)
    while len(movies_list) < 3:
        random_movie = movies[random.randrange(0, len(movies))]
        if random_movie not in movies_list:
            movies_list.append(random_movie)

    context = {
        'recommend_movie': movies_list[:3],
    }
    return render(request, 'movies/recommend.html', context)


@require_POST
def comments_create(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        comment_form = MovieCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.title = movie
            comment.user = request.user
            comment.save()
        return redirect('movies:detail', movie.pk)
    return redirect('accounts:login')


@require_POST
def comments_delete(request, movie_pk ,comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(MovieComment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_pk)


@login_required
@require_http_methods(["GET", "POST"])
def comments_update(request, movie_pk, comment_pk):
    comment = MovieComment.objects.get(pk = comment_pk)
    if request.method == "POST":
        form = MovieCommentForm(request.POST, instance = comment)
        if form.is_valid():
            form.save()
            return redirect('movies:detail', movie_pk)

    return_form = MovieCommentForm(instance = comment)
    context = {
        'form':return_form,
    }
    return render(request, 'movies/comments_update.html', context)


@require_GET
def index_best(request):
    movies = Movie.objects.order_by('vote_average')
    if not movies:
        call_command('loaddata', genres_fixture, app_label='movies')
        call_command('loaddata', movies_fixture, app_label='movies')
        movies = Movie.objects.order_by('vote_average')

    context = {
        'movies': movies,
    }
    return render(request, 'movies/index_best.html', context)


@require_GET
def index_date(request):
    movies = Movie.objects.order_by('release_date')
    if not movies:
        call_command('loaddata', genres_fixture, app_label='movies')
        call_command('loaddata', movies_fixture, app_label='movies')
        movies = Movie.objects.order_by('release_date')

    context = {
        'movies': movies,
    }
    return render(request, 'movies/index_date.html', context)