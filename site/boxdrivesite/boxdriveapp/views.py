import os
#import magic
#import mimetypes
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from encrypted_files.uploadhandler import EncryptedFileUploadHandler
from django.urls import reverse

from . models import Document
from django.contrib.auth.models import User
from boxdriveusersreg.models import Profile
from boxdrivesite.settings import MEDIA_ROOT
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.core.files.uploadhandler import MemoryFileUploadHandler, TemporaryFileUploadHandler
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from encrypted_files.base import EncryptedFile
from django.http import HttpResponse


def about(request):
    return render(request, 'boxdriveapp/about.html')


##################################################################
class DocumentListView(LoginRequiredMixin, ListView):
    model = Document
    template_name = 'boxdriveapp/home.html'
    context_object_name = 'documents'

    # функция для фильтрации документов по юзеру 
    def get_queryset(self, *args, **kwargs):
        return Document.objects.filter(cur_user=self.request.user.profile).order_by('-upload_time')


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


class DocumentDeleteView(LoginRequiredMixin, DeleteView):
    model = Document

    def get(self, request, pk):
        object = self.get_object()
        if object is not None:
            # TODO: actually remove file from fs
            object.delete()
            messages.success(request, 'Your post has been deleted successfully.')
            return redirect('boxdrive-home')
        else:
            messages.success(request, "Something went wrong. Couldn't delete file.")

#################################################################


@method_decorator(csrf_exempt, 'dispatch')
class CreateEncryptedFile(CreateView):
    model = Document
    fields = ["file"]

    def post(self, request, *args, **kwargs):
        request.upload_handlers = [
            EncryptedFileUploadHandler(request=request),
            MemoryFileUploadHandler(request=request),
            TemporaryFileUploadHandler(request=request)
        ]  
        return self._post(request)

    @method_decorator(csrf_protect)
    def _post(self, request):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def decrypted(request,pk):
    f = Document.objects.get(pk=pk).file_field
    ef = EncryptedFile(f)
    return HttpResponse(ef.read()), f

class DocumentDownloadView(UpdateView):
    def get(self, request, pk):
        response , f = decrypted(request, pk)
        response['Content-Disposition'] = 'attachment; filename={file}'.format(file=f)
        response['Content-Type'] = "text\plain"
        return response