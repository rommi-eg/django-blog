from django.contrib import admin
from .models import Post, Comment


@admin.register(Post) # регистрирует модель в панели администратора
class PostAdmin(admin.ModelAdmin):
    """ Класс внешнего вида модели Post в панели администратора """

    # Позволяет задавать поля модели, которые отобразятся на
    # странице списка объектов администрирования.
    list_display = (  
        'title', 'slug', 'author', 'publish', 'status',
    )

    # Создает фильтр в панели администратора по 
    # указанным полям.
    list_filter = (
        'status', 'created', 'publish', 'author',
    )

    # Добавляет строку поиска и определяет список полей,
    # по которым будет происходить поиск.
    search_fields = (
        'title', 'body',
    )

    # Позволяет автоматически заполнять поле slag при
    # вводе заголовка статьи.
    prepopulated_fields = {
        'slug': ('title',),
    }

    # Задает отображение поля поисковым виджетом.
    raw_id_fields = (
        'author',
    )

    # Добавляет навигационные ссылки по иерархии дат.
    date_hierarchy = 'publish'

    # Задает критерии сортировки, которые будут использованы
    # по умолчанию.
    ordering = (
        'status', 'publish',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'email', 'post', 'created', 'active'
    )
    list_filter = (
        'active', 'created', 'updated'
    )
    search_fields = (
        'name', 'email', 'body'
    )
