from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post


def post_list(request):
    """ Представление списка постов на странице """

    # Извлекаем все посты со статусом PUBLISHED
    # используя созданый ранее менеджер
    posts = Post.published.all()

    # Постраничная разбивка с 3 постами на странице
    painator = Paginator(posts, 3)

    # Извлекаем GET-параметр page и сохраняем его в переменной page_number
    # Этот параметр содержин запрошеный номер страницы. Если параметра нет
    # то используется стандартное значение 1, чтобы загрузить первую страницу.
    page_number = request.GET.get('page', 1)

    try:
        # Получаем объект для желаемой страницы, вызывая метод page()
        # класса Paginator, который возвращает объект Page
        posts = painator.page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое число, то выдать первую страницу
        posts = painator.page(1)
    except EmptyPage:
        # Если page_number находиться вне диапазона, то
        # выдать последнюю страницу
        posts = painator.page(painator.num_pages)

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
