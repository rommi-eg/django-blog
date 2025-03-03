from django.shortcuts import render, get_object_or_404
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
    
    # Извлекаем объект, соответствующий переданным параметрам.
    # Если объект не найден вернется мсключение HTTP с кодом
    # состояния 404.
    post = get_object_or_404(
        Post, id=id, status=Post.Status.PUBLISHED,
    )
    
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post},
    )
