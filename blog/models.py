from django.db import models
from users.models import UserProfile

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    cover_photo = models.ImageField(upload_to='blog_covers/')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='blog_posts')
    likes = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.first_name} {self.author.last_name} on {self.blog_post.title}'
