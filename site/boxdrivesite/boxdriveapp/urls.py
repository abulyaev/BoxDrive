from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='boxdrive-home'),
    path('about/', views.about, name='boxdrive-about'),
]