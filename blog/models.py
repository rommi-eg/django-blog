from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    """ Модель поста в базе данных """

    # Заголовок поста. Поле с типом CharField, которое
    # транслируется в солбец VARCHAR в базе данных SQL.
    title = models.CharField(
        max_length=255, # максиьвльная длина 255 символов
    )

    # Поле с типом SlugField, которое транслируется в солбец
    # VARCHAR в базе данных SQL. Слаг - это метка содержащая
    # только буквы, цифры, знаки подчеркивания или дефисы.
    # Пример: django-reinhardt-legend-jazz
    slug = models.SlugField(
        max_length=255,
    )

    # Поле для хранения тела поста. Поле с типом TextField
    # транслируется в солбец Text в базе данных SQL.
    body = models.TextField(
        default='Скоро здесь будет статья...' # значение по умолчанию
    )

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
    updatet = models.DateTimeField(
        auto_now=True # дата будет обновляться автоматически во время сохранения объекта
    )

    class Meta:
        """ Класс определяет метаданные модели """

        # Атрибут сортировки результата. Данный порядок применяется
        # по умолчанию для запросов к базе данных, если не указан
        # конкретный порядок.
        ordering = [
            '-publish' # поле, по которому будет происходить сортировка
        ]

    def __str__(self):
        """ Возвращает строковый литерал объекта в удобочитаемом представлении """
        return self.title
