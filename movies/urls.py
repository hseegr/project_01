from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='movie_detail'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('<int:movie_pk>/likes/', views.likes, name='likes'),
    path('<int:movie_comment_pk>/movie_comments/', views.movie_comments_create, name='movie_comments_create'),
    path('<int:movie_pk>/movie_comments/<int:movie_comment_pk>/delete/', views.movie_comments_delete, name='movie_comments_delete'),
    path('weather_input/', views.weather_input, name='weather_input'),
    path('weather/<str:city>/', views.weather_view, name='weather'),
    # path('weather/filter/', views.filtered_movies, name='filtered_movies'),
    path('movie_record/', views.movie_record, name='movie_record'),
    # path('create/', views.create, name='create'),
    # path('<int:pk>/delete/', views.delete, name='delete'),
    # path('<int:pk>/update/', views.update, name='update'),
]