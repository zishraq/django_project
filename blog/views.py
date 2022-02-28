from django.shortcuts import render
from django.http import HttpResponse


posts = [
    {
        'author': 'Zuhair Ishraq',
        'title': 'Blog Post 1',
        'content': '1 post content',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'Marcus Aurelius',
        'title': 'Blog Post 2',
        'content': '2 post content',
        'date_posted': 'August 30, 2018'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html')
