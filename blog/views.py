from django.shortcuts import render
from .models import Post


# Create your views here.
def post_list(request):
    """ Представление списка постов на странице """

    # Извлекаем все посты со статусом PUBLISHED
    posts = Post.published.all() # ипользуется созданый ранее менеджер
    return render(
        request=request, # принимаемый объект request
        template_name='blog/post/list.html', # путь к шаблону
        context={'posts': posts}, # контекстные переменные, чтобы прорисовать даннный щаблон
    )
