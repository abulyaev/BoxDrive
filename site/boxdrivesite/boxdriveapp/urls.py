from django.urls import path
from .views import PostListView, PostDetailView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='boxdrive-home'),
    path('file/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('', views.home, name='boxdrive-home'),
    path('about/', views.about, name='boxdrive-about'),
]