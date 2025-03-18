from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm
from taggit.models import Tag


def post_list(request, tag_slug=None):
    """ Представление списка постов на странице """

    # Извлекаем все посты со статусом PUBLISHED
    # используя созданый ранее менеджер
    posts = Post.published.all()

    tag = None

    if tag_slug:
        # Извлекаем объекты tag с полученым слагом
        tag = get_object_or_404(Tag, slug=tag_slug)
        # Фильтруем посты по тегам
        posts = posts.filter(tags__in=[tag])

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
        'posts': posts, 'tag': tag
    }

    # Шаблон в котором прорисовывается контекст
    template = 'blog/post/list.html'

    return render(request=request, template_name=template, context=context)


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

    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)

    # Форма для комментирования пользователями
    form = CommentForm()

    # Получаем список идентификаторов тегов текущего поста.
    # values_list() - возвращает кортежи со значениями заданных полей
    # float=True - чтобы получить одиночные значения [1, 2, 3, ...]
    post_tag_ids = post.tags.values_list('id', flat=True)

    # Берутся все посты, содержащие любой из этих тегов, за исключением
    # текущего поста
    similar_posts = Post.published.filter(tags__in=post_tag_ids
    ).exclude(id=post.id)

    # Применяется функция агрегирования Count. Её работа - генерировать
    # вычисляемое поле - same_tags, которое содержит число тегов, общих
    # со всеми запрошенными тегами. Результат упорядочивается по числу
    # общих тегов (в убывающем порядке). Резульнат нарезается, чтобы
    # получить только первые четыре поста
    similar_posts = similar_posts.annotate(same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    # Контекстные переменные, чтобы прорисовать шаблон
    context = {
        'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts
    }

    # Шаблон в котором прорисовывается контекст
    template = 'blog/post/detail.html'
    
    return render(request=request, template_name=template, context=context)


def post_share(request, post_id):
    """ Представление обрабатывающее форму отправки письма с рекомендациями """

    # Получаем пост по идентификатору id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Поля формы успешно прошли валидацию
            cd = form.cleaned_data

            # Получаем абсолютный путь к посту
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )

            # Создаем тему сообщения
            subject = (
                f'{cd['name']} recommends you read {post.title}'
            )

            # Создаем текст сообщения
            message = (
                f'Read {post.title} at {post_url}\n\n'
                f'{cd['name']}\'s comments: {cd['comments']}'
            )

            # Отправляем электронное письмо
            send_mail(
                subject=subject, # Тема
                message=message, # Сообщение
                from_email=settings.EMAIL_HOST_USER, # почта отправки сообщений
                recipient_list=[cd['to']] # кому отправлять сообщение
            )

            sent = True
    else:
        form = EmailPostForm()

    context = {'post': post, 'form': form, 'sent': sent}

    template = 'blog/post/share.html'

    return render(request=request, template_name=template, context=context)


@require_POST
def post_comment(request, post_id):
    """ Представление для отиравки комментария """

    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )

    comment =None

    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()

    context = {'post': post, 'form': form, 'comment': comment}

    template = 'blog/post/comment.html'

    return render(request=request, template_name=template, context=context)


def post_search(request):
    """ Представление для поиска """

    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    
    context = {'form': form, 'query': query, 'results': results}

    template = 'blog/post/search.html'

    return render(request=request, template_name=template, context=context)