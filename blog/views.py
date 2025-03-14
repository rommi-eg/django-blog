from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """ Представление списка постов на странице """

    # Извлекаем все посты со статусом PUBLISHED
    # используя созданый ранее менеджер
    posts = Post.published.all()

    # Контекстные переменные, чтобы прорисовать шаблон
    context = {
        'posts': posts,
    }

    # Шаблон в котором прорисовывается контекст
    template = 'blog/post/list.html'

    return render(request=request, template_name=template, context=context)


def post_detail(request, year, month, day, post):
    """ Представление одиночного поста на странице """

    # Извлекаем объект, соответствующий переданным параметрам.
    # Если объект не найден вернется мсключение HTTP с кодом
    # состояния 404.
    post = get_object_or_404(
        Post,  
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # Контекстные переменные, чтобы прорисовать шаблон
    context = {
        'post': post,
    }

    # Шаблон в котором прорисовывается контекст
    template = 'blog/post/detail.html'
    
    return render(request=request, template_name=template, context=context)
