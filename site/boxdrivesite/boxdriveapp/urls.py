from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='boxdrive-home'),
    path('file/new/', PostCreateView.as_view(), name='post-create'),
    path('file/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('file/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('file/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('', views.home, name='boxdrive-home'),
    path('about/', views.about, name='boxdrive-about'),
]