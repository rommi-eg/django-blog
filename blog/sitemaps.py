from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSitemap(Sitemap):
    """ Класс кары сайта """

    # Атрибуты указывают частоту изменения страниц постов
    # и их релевантность на веб-сайте (макс. значение равно 1)
    # Атрибуты changefreq и priority могут быть методами
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        """ Возвращает объекты, подлежащие вулючению в карту сайта """
        return Post.published.all()
    
    def lastmod(self, obj):
        """ Возвращает время последнего изменения объекта """
        return obj.updated