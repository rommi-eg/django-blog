from django.urls import path

from . import views


app_name = 'blog'


urlpatterns = [
    # Шаблон url-адреса, который не принимает аргументов
    # и соотносится с представлением post_list 
    path('', view=views.post_list, name='post_list'),

    # Шаблон url-адреса, который не принимает один аргумент
    # id и соотносится с представлением post_detail
    path('<int:id>/', view=views.post_detail, name='post_detail'),
]
