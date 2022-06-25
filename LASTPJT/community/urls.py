from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'community'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:community_pk>/', views.detail, name='detail'),
    path('<int:community_pk>/delete/', views.delete, name='delete'),
    path('<int:community_pk>/update/', views.update, name='update'),
    path('<int:community_pk>/like/', views.like, name='like'),
    path('<int:community_pk>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:community_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),
    path('notice/', views.index_commu1, name='index_commu1'),
    path('chat/', views.index_commu2, name='index_commu2'),
    path('review/', views.index_commu3, name='index_commu3'),
    path('event/', views.index_commu4, name='index_commu4'),
    path('other/', views.index_commu5, name='index_commu5'),
    path('<int:community_pk>/comments/<int:comment_pk>/update/', views.comments_update, name = 'comments_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
