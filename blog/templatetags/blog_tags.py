from django import template

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
def total_posts():
    """ Возвращает число опубликованных постов """
    return Post.published.count()