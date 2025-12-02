from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()[:5]  # Get latest 5 posts
    context = {
        'posts': posts,
        'title': 'Home'
    }
    return render(request, 'blog/index.html', context)
