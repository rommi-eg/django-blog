from django.db import models

# Create your models here.
class Post(models.Model):
    """ Модель поста в базе данных """

    # Заголовок поста. Поле с типом CharField, которое
    # транслируется в солбец VARCHAR в базе данных SQL
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
    # транслируется в солбец Text в базе данных SQL
    body = models.TextField(
        default='Скоро здесь будет статья...' # значение по умолчанию
    )

    def __str__(self):
        """ Возвращает строковый литерал объекта в удобочитаемом представлении """
        return self.title
