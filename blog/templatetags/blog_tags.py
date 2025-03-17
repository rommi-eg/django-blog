import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post


# В каждом содержащем шаблонные теги модуле должна быть определена
# переменная с именем register. Эта переменная является экземпляром
# класса template.Library и  используется для регистрации шаблонных
# тегов и фильтров приложения.
register = template.Library()


# Регистрируем как простой тег. Django будет использовать имя функции
# в качестве имени тега. Если нужно зарегистрировать под другим именем
# нужно указать атрибут name, например @register.simple_tag(name='my_tag')
@register.simple_tag
def total_posts() -> int:
    """ Возвращает количество опубликованных постов """
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """ Возвращает последние опубликованные посты """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """ Возвращает посты с наибольшим числом комментариев """
    return Post.published.annotate(total_comments=Count('comments')
                                   ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """ Фильтр для конвертации markdown в html"""
    return mark_safe(markdown.markdown(text=text, extensions=['extra', 'codehilite']))
