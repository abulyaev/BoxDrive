from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from . models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['fileName', 'fileUrl']

    def form_valid(self, form):
        form.instance.poster = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['fileName', 'fileUrl']

    def form_valid(self, form):
        form.instance.poster = self.request.user
        return super().form_valid(form)

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.poster:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.poster:
            return True
        return False


def about(request):
    return render(request, 'boxdriveapp/about.html')
