from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from . models import Post, Document
from django.contrib.auth.models import User
from boxdriveusersreg.models import Profile
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


def about(request):
    return render(request, 'boxdriveapp/about.html')


##################################################################
class DocumentListView(ListView):
    model = Document
    template_name = 'boxdriveapp/home.html'
    context_object_name = 'documents'

    # функция для фильтрации документов по юзеру 
    def get_queryset(self, *args, **kwargs):
        return Document.objects.filter(cur_user=self.request.user.profile)


class DocumentDetailView(DetailView):
    model = Document


class DocumentCreateView(LoginRequiredMixin, CreateView):
    model = Document
    fields = ['title', 'file_field']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DocumentUploadView(UpdateView):
    def get(self, request, cur_user, *args, **kwargs):
        return render(request, 'boxdriveapp/upload_file.html', {'cur_user': cur_user,})

    def post(self, request, cur_user):
        filename = request.FILES['filename']
        title = request.POST['title']

        user_obj = Profile.objects.get(user__username=cur_user)
        upload_doc = Document(cur_user=user_obj, title=title, file_field=filename)
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

