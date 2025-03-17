from django.urls import path

from . import views
from .feeds import LatestPostaFeed


app_name = 'blog'


urlpatterns = [
    # Шаблон url-адреса, который не принимает аргументов
    # и соотносится с представлением post_list 
    path('', view=views.post_list, name='post_list'),

    # Шаблон url-адреса, который не принимает аргументов
    # и соотносится с представлением рефлизованным в виде класса
    # PostListView
    # path('', view=views.PostListView.as_view(), name='post_list'),

    # Шаблон url-адреса, который принимает один аргумент
    # id и соотносится с представлением post_detail
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', view=views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', view=views.post_share, name='post_share'),
    path('<int:post_id>/comment/', view=views.post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', view=views.post_list, name='post_list_by_tag'),
    path('feed/', view=LatestPostaFeed(), name='post_feed'),
]
