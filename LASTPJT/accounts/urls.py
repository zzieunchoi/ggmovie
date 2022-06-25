from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<int:user_pk>/', views.profile, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<int:user_pk>/profile_create/', views.profile_create, name="profile_create"),
    path('<int:user_pk>/<int:profile_pk>/profile_update/', views.profile_update, name = 'profile_update'),
    path('<int:user_pk>/<int:profile_pk>/profile_delete/', views.profile_delete, name = 'profile_delete'),
]
