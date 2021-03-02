from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . models import Post

def home(request):

    context = {
        'files': Post.objects.all()
    }
    return render(request, 'boxdriveapp/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'boxdriveapp/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'files'
    ordering = ['-datePosted']


class PostDetailView(DetailView):
    model = Post


def about(request):
    return render(request, 'boxdriveapp/about.html')
