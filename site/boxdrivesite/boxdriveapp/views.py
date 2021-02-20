from django.shortcuts import render
from . models import Post

def home(request):

    context = {
        'files': Post.objects.all()
    }
    return render(request, 'boxdriveapp/home.html', context)

def about(request):
    return render(request, 'boxdriveapp/about.html')