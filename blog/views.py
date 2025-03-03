from django.shortcuts import render
from django.http import Http404
from .models import Post


# Create your views here.
def post_list(request):
    """ Представление списка постов на странице """

    # Извлекаем все посты со статусом PUBLISHED
    posts = Post.published.all() # ипользуется созданый ранее менеджер

    return render(
        request=request, # принимаемый объект request
        template_name='blog/post/list.html', # путь к шаблону
        context={'posts': posts}, # контекстные переменные, чтобы прорисовать даннный щаблон
    )


def post_detail(request):
    """ Представление одиночного поста на странице """

    try:
        # пытаемся извлечь объект Post с заданным id
        post = Post.published.get(id=id)
    except Post.DoesNotExist: # если возникнет исключение DoesNotExist
        # поднимаем исключение и возвращаем ошибку HTTP
        # с кодом состояния 404
        raise Http404('No Post found')
    
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post},
    )
