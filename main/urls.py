from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('details/<int:id>/', views.MovieDetailView.as_view(), name='detail'),
    path('addmovie/', views.AddMovieView.as_view(), name='add_movie'),
    path('editmovie/<int:id>', views.EditMovieView.as_view(), name='edit_movie'),
    path('deletemovie/<int:id>', views.DeleteMovieView.as_view(), name='delete_movie'),
    path('addreview/<int:id>', views.AddReviewView.as_view(), name='add_review'),
    path('editreview/<int:movie_id>/<int:review_id>/', views.EditReviewView.as_view(), name='edit_review'),
    path('deletereview/<int:movie_id>/<int:review_id>/', views.DeleteReviewView.as_view(), name='delete_review')
]
