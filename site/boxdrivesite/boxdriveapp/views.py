from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from . models import Post, Document
from boxdriveusersreg.models import Profile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def home(request):

    context = {
        'files': Post.objects.all()
    }
    return render(request, 'boxdriveapp/home.html', context)


def about(request):
    return render(request, 'boxdriveapp/about.html')

##################################################################
class DocumentListView(ListView):
    model = Document
    template_name = 'boxdriveapp/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'files'
    #ordering = ['pk']


class DocumentDetailView(DetailView):
    model = Document


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['title', 'file_field']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DocumentUploadView(ListView):
    def get(self, request, username):
        return render(request, 'boxdriveapp/upload_file.html')


    def post(self, request, username):
        filename = request.FILES['filename']
        title = request.POST['title']

        user_obj = Profile.objects.get(username=username)
        upload_doc = Document(user=user_obj, title=title, file_field=filename)
        upload_doc.save()
        messages.success(request, 'Your Post has been uploaded successfully.')
        return render(request, 'boxdriveapp/upload_file.html')


class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Document

    def get(self, request, document_id):
        user = request.session['user']
        delete_doc = self.model.objects.get(id=document_id)
        delete_doc.delete()
        messages.success(request, 'Your post has been deleted successfully.')
        return redirect(f'')

#################################################################


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

