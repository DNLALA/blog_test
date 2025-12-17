from django.urls import path
from blog.api import views

urlpatterns = [
    path('posts_create/', views.BlogPostCreateAPIView.as_view(), name='blogpost-create'),
    path('posts_list/', views.BlogPostListAPIView.as_view(), name='blogpost-list'),
    path('comments/', views.CommentListCreateAPIView.as_view(), name='comment-list-create'),
]
