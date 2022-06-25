from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.index, name='index'),
    path('list/best/', views.index_best, name='index_best'),
    path('list/date/', views.index_date, name='index_date'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/recommend/', views.recommend, name='recommend'),
    path('<int:movie_pk>/comments/create/', views.comments_create, name='comments_create'),
    path('<int:movie_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:movie_pk>/comments/<int:comment_pk>/update/', views.comments_update, name = 'comments_update'),
]
