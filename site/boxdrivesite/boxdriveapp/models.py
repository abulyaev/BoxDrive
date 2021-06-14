from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from boxdriveusersreg.models import Profile
from django.urls import reverse


# TODO: Here we need to discuss about fields
class Document(models.Model):
    objects = models.Manager()
    cur_user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    file_field = models.FileField(upload_to='documents/')
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document-detail', kwargs={'pk': self.pk})