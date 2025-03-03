from django.shortcuts import render
from .models import Post


# Create your views here.
def post_list(request):
    """ Представление списка постов на странице """
    posts = Post.published.all()
    return render(
        request=request,
        template_name='blog/post/list.html',
        context={'posts': posts},
    )
