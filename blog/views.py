from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post


# Create your views here.
def post_list(request):
    """ Представление списка постов на странице """

    # Извлекаем все посты со статусом PUBLISHED
    posts = Post.published.all() # ипользуется созданый ранее менеджер

    # Постраничная разбивка с 3 постами на странице
    paginator = Paginator(posts, 3)

    # Извлекаем GET-параметр page и сохраняем его в переменной page_number
    # Этот параметр содержин запрошеный номер страницы. Если параметра нет
    # то используется стандартное значение 1, чтобы загрузить первую страницу. 
    page_number = request.GET.get('page', 1)

    try:
        # Получаем объекты для желаемой страницы, вызвав метод get_page()
        posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Если page_number не целое чистло, то
        # выдать первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу.
        posts = paginator.page(paginator.num_pages)

    return render(
        request=request, # принимаемый объект request
        template_name='blog/post/list.html', # путь к шаблону
        context={'posts': posts}, # контекстные переменные, чтобы прорисовать даннный щаблон
    )


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
        publish__day=day,
    )
    
    return render(
        request=request,
        template_name='blog/post/detail.html',
        context={'post': post},
    )


# Альтернативное представление списка постов реализованное в виде класса
class PostListView(ListView):
    """ Класс представления списка постов """

    # Атрибут используется  для того, чтобы иметь конкретно-прикладной
    # набор запросов QyerySet, не извлекая все объекты. Вместо определения
    # атрибута queryset мы могли бы указать model=Post, и Django сформировал
    # бы типовой набор запросов Post.objects.all()
    queryset = Post.published.all()

    # Контекстная переменная, используется для результатов запроса.
    # Если не указана, то по умолчанию исрользуется переменная object_list. 
    context_object_name = 'posts'

    # Задает постраничную разбивку результатов с возвратом
    # (в данном случае) 3 объектов.
    paginate_by = 3

    # Шаблон для прорисовки страницы
    template_name = 'blog/post/list.html'
    
