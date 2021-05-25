from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db.models import Avg
from .models import *
from .forms import *


# Create your views here.

class HomeView(View):
    def get(self, request):
        query = request.GET.get('title')
        all_movies = None

        if query:
            all_movies = Movie.objects.filter(name__icontains=query)
        else:
            all_movies = Movie.objects.all()

        context = {
            'movies': all_movies,
        }

        return render(request, 'main/index.html', context)


class MovieDetailView(View):
    def get(self, request, id):
        movie = Movie.objects.get(id=id)
        reviews = Review.objects.filter(movie=id).order_by('-date')

        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            average_rating = round(average_rating, 2)
        else:
            average_rating = 0

        context = {
        'movie': movie,
        'reviews': reviews,
        'average_rating': average_rating
        }

        return render(request, 'main/details.html', context)

class AddMovieView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                form = MovieForm()

                return render(request, 'main/addmovie.html', {'form': form, 'controller': 'Add Movie'})
            else:
                return redirect('main:home')
        else:
            return redirect('accounts:login')

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                form = MovieForm(request.POST or None)

                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()

                    return redirect('main:home')

                return render(request, 'main/addmovie.html', {'form': form, 'controller': 'Add Movie'})
            else:
                return redirect('main:home')
        else:
            return redirect('accounts:login')


class EditMovieView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                movie = Movie.objects.get(id=id)               
                form = MovieForm(instance=movie)

                return render(request, 'main/addmovie.html', {'form': form, 'controller': 'Edit Movie'})
            else:
                return redirect('main:home')
        else:
            return redirect('accounts:login')

    def post(self, request, id):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                movie = Movie.objects.get(id=id)
                form = MovieForm(request.POST or None, instance=movie)

                if form.is_valid():
                    data = form.save()
                    data.save()

                    return redirect('main:detail', id)
                
                return render(request, 'main/addmovie.html', {'form': form, 'controller': 'Edit Movie'})
            else:
                return redirect('main:home')
        else:
            return redirect('accounts:login')
        

class DeleteMovieView(View):
    def get(self, request, id):        
        if request.user.is_authenticated:
            if request.user.is_superuser:
                movie = Movie.objects.get(id=id)

                movie.delete()

                return redirect('main:home')
            else:
                return redirect('main:home')
        else:
            return redirect('accounts:login')


class AddReviewView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            movie = Movie.objects.get(id=id)
            form = ReviewForm()

            return render(request, 'main/details.html', {'form': form})
        else: 
            return redirect('accounts:login')

    def post(self, request, id):
        if request.user.is_authenticated:
            movie = Movie.objects.get(id=id)
            form = ReviewForm(request.POST or None)

            if form.is_valid():
                data = form.save(commit=False)
                data.comment = request.POST['comment']
                data.rating = request.POST['rating']
                data.user = request.user
                data.movie = movie
                data.save()

                return redirect('main:detail', id)

            return render(request, 'main/details.html', {'form': form})
        else: 
            return redirect('accounts:login')    


class EditReviewView(View):
    def get(self, request, movie_id, review_id):
        if request.user.is_authenticated:
            movie = Movie.objects.get(id=movie_id)
            review = Review.objects.get(movie=movie, id=review_id)

            if request.user == review.user:
                form = ReviewForm(instance=review)
                
                return render(request, 'main/editreview.html', {'form': form})
            else:
                return redirect('main:detail', movie_id)
        else:
            return redirect('accounts:login')

    def post(self, request, movie_id, review_id):
        if request.user.is_authenticated:
            movie = Movie.objects.get(id=movie_id)
            review = Review.objects.get(movie=movie, id=review_id)

            if request.user == review.user:
                form = ReviewForm(request.POST, instance=review)

                if form.is_valid():
                    data = form.save(commit=False)
                    if (data.rating > 10) or (data.rating < 0):
                        error = 'Out of range. Please select rating from 0 to 10.'
                        
                        return render(request, 'main/editreview.html', {'error': error, 'form': form})
                    else:
                        data.save()

                        return redirect('main:detail', movie_id)
            else:
                return redirect('main:detail', movie_id)
        else:
            return redirect('accounts:login')       

class DeleteReviewView(View):
    def get(self, request, movie_id, review_id):
        if request.user.is_authenticated:
            movie = Movie.objects.get(id=movie_id)
            review = Review.objects.get(movie=movie, id=review_id)

            if request.user == review.user:
                review.delete()

            return redirect('main:detail', movie_id)
        else:
            return redirect('accounts:login')
