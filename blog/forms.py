from django import forms

from .models import Comment


class EmailPostForm(forms.Form):
    """ Класс формы позволяющей дплиться постами """

    # Экземпляр класса CharField с максимальной длиенной 25 символов,
    # который будет использоваться для имени человека, отправляющего
    # письмо. 
    # Поле этого типа прорисовывается HTML-элемент <input type="text">
    name = forms.CharField(
        max_length=25
    )

    # Экземпляр класс EmailField. Здесь адрес электонной почты, человека
    # отправившего рекомендательный пост.
    email = forms.EmailField()

    # Экземпляр класс EmailField. Здесь адрес электонной почты, человека,
    # который будет получать письмо с рекомендуемым постом.
    to = forms.EmailField()

    # Экземпляр класс CharField. Используется для коммениариев, которые
    # будут вставляться электонное письмо с рекомендуемым постом.
    comments = forms.CharField(
        required=False, # опциональное поле
        # Виджет прорисовки поля в HTML. Будет отображаться как HTML-элемент
        # <textarea> вместо используемого по умолчанию элемента input.
        widget=forms.Textarea
    )


class CommentForm(forms.ModelForm):
    """ Класс формы отправки комментария """

    class Meta:
        model = Comment # модель из которой будет создана форма
        fields = [
            'name', 'email', 'body' # поля которые будут включены в форму
        ]


class SearchForm(forms.Form):
    """ Класс формы поиска """
    query = forms.CharField()
