from django.urls import path
from blog.api import views

urlpatterns = [
    path("blogpost-like/<int:pk>/", views.BlogPostLikeToggleAPIView.as_view(), name="blogpost-like"),
    path('blogpost-create/', views.BlogPostCreateAPIView.as_view(), name='blogpost-create'),
    path('posts_list/', views.BlogPostListAPIView.as_view(), name='blogpost-list'),
    path('comments-create/', views.CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments-list/', views.CommentListAPIView.as_view(), name='comment-list'),
]
