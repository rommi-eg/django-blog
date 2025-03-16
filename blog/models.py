from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager



class PublishedManager(models.Manager):
    """ Класс модельного менеджера. Позволяет извлекать посты со статусом PUBLISHED """
    
    def get_queryset(self):
        """ Возвращает набор запросов QuerySet, который будет исполнен """
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):
    """ Класс поста в базе дагнных """

    class Status(models.TextChoices):
        """ Подкласс перечисления статуса """

        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    # Заголовок поста. Поле с типом CharField, которое
    # транслируется в солбец VARCHAR в базе данных SQL
    title = models.CharField(
        max_length=255, # максимальная длина 255 символов
    )

    # Поле с типом SlugField, которое транслируется в солбец
    # VARCHAR в базе данных SQL. Слаг - это метка содержащая
    # только буквы, цифры, знаки подчеркивания или дефисы.
    # Пример: django-reinhardt-legend-jazz
    slug = models.SlugField(
        max_length=255,
        unique_for_date='publish' # делает поле slug уникальным для даты сохраненной в поле publish
    )

    # Поле для хранения тела поста. Поле с типом TextField
    # транслируется в солбец Text в базе данных SQL.
    body = models.TextField()

    # Поле для хранения даты и времени публикации поста.
    # Поле с типом DateTimeField транслируется в солбец
    # DATETIME в базе данных SQL.
    publish = models.DateTimeField(
        default=timezone.now # возвращает текущую дату/время в формате, зависящем от часового пояса
    )

    # Поле для хранения даты и времени создания поста.
    # Поле с типом DateTimeField транслируется в солбец
    # DATETIME в базе данных SQL.
    created = models.DateTimeField(
        auto_now_add=True # дата будет сохраняться автоматически во время создания объекта
    )

    # Поле для хранения даты и времени обновления поста.
    # Поле с типом DateTimeField транслируется в солбец
    # DATETIME в базе данных SQL.
    updated = models.DateTimeField(
        auto_now=True # дата будет обновляться автоматически во время сохранения объекта
    )

    # Поле для хранения статуса поста. Поле с типом CharField,
    # которое транслируется в солбец VARCHAR в базе данных SQL.
    status = models.CharField(
        max_length=2,
        choices=Status.choices, # ограничивает значение поля вариантами из Status.choices
        default=Status.DRAFT, # значение по умолчанию
    )

    # Поле определяет взаимосвязь многие-к-одному, означающую,
    # что каждый пост написан пользователем и каждый пользователь
    # может написать лкбое количетво постов.
    author = models.ForeignKey( # внешний кдюч в базе данных
        to=User, # молель на которую ссылается внешний ключ
        on_delete=models.CASCADE, # при удалении пользователя, удалятся связанные с ним посты
        related_name='blog_posts', # имя обратной связи, от  User к Post (по сути это имя таблицы в базе)
    )

    objects = models.Manager() # стандарный менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер
    tags = TaggableManager() # этот менеджер позволит добавлять, извлекать и удалять теги из объекта Post

    class Meta:
        """ Класс определяет метаданные модели """

        # Атрибут сортировки результата. Данный порядок применяется
        # по умолчанию для запросов к базе данных, если не указан
        # конкретный порядок.
        ordering = [
            '-publish' # поле, по которому будет происходить сортировка
        ]

        # Атрибут позволяет определять в модели индексы базы данных,
        # которые могут содержать одно или несколько полей в возрастающем
        # либо убывающем порядке, или функциональные выражения и функции
        # базы данных.
        # Индексное упорядочивание не работает в базе данных MySQL.
        indexes = [
            models.Index(
                fields=['-publish'] # поле по которому будет проходить индексация
            )
        ]

    def __str__(self):
        """ Возвращает строковый литерал объекта в удобочитаемом представлении """
        return self.title
    
    def get_absolute_url(self):
        """ Возвращает канонический url-адрес объекта """
        return reverse('blog:post_detail', args=[
            self.publish.year, 
            self.publish.month, 
            self.publish.day,
            self.slug
            ]
        )


class Comment(models.Model):
    """ Модель комментария к посту """

    # Поле, чтобы связать каждый комментарий с одним постом.
    # Указанная взаимосвязь многие-к-одному, потому что кахдый
    # комментарий будет делаться к одному посту, и каждый пост
    # может содержать несколько комментариев
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(
        max_length=80
    )
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    # Булево поле, чтобы управлять статусом комментариев.
    # Данное поле позволит деактивировать неуместные
    # комментарии вручную с помощью админ панели
    active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
 