import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars_html
from django.urls import reverse_lazy

from .models import Post


class LatestPostaFeed(Feed):
    """ Класс новостной ленты """

    # Атрибуты соответстиуют элементам RSS
    title = 'My blog'
    link = reverse_lazy('blog:post_list') # генерирует url-адреса
    description = 'New posts of my blog.'

    def items(self):
        """ Возвращает включаемые в новостную ленту объекты """
        return Post.published.all()[:5]
    
    def item_title(self, item):
        """ Возвращает заголовок объекта """
        return item.title
    
    def item_description(self, item):
        """ Возвращает описание объекта """
        return truncatechars_html(markdown.markdown(item.body), 30)
    
    def item_pubdata(self, item):
        """ Возвращает дату публикации объекта """
        return item.publish