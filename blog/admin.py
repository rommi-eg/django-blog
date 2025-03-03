from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post) # регистрирует модель в панели администратора
class PostAdmin(admin.ModelAdmin):
    """ Класс внешнего вида модели в панели администратора """

    # Позволяет задавать поля модели, которые отобразятся на
    # странице списка объектов администрирования.
    list_display = (  
        'title', 'slug', 'author', 'publish', 'status',
    )
