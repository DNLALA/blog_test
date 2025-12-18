from rest_framework import serializers
from users.models import UserProfile
from users.api.user_profile.serializers import UserProfileSerializer
from blog.models import BlogPost, Comment


class JustBlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'cover_photo', 'author', 'likes', 'created_at', 'updated_at']



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'blog_post', 'body', 'author', 'created_at']

class CommentGetSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    blog_post = JustBlogPostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'blog_post', 'body', 'author', 'created_at']

class BlogPostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    likes = serializers.StringRelatedField(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'cover_photo', 'author', 'likes', 'comments', 'created_at', 'updated_at']

class BlogPostGetSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer(read_only=True)
    likes = serializers.StringRelatedField(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'body', 'cover_photo', 'author', 'likes', 'comments', 'created_at', 'updated_at']


class BlogPostLikeToggleSerializer(serializers.Serializer):
    liked = serializers.BooleanField(read_only=True)
    likes_count = serializers.IntegerField(read_only=True)
    message = serializers.CharField(read_only=True)

    def save(self, **kwargs):
        request = self.context["request"]
        blog_post = self.context["blog_post"]
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile = user_profile

        if blog_post.likes.filter(id=user_profile.id).exists():
            blog_post.likes.remove(user_profile)
            return {
                "liked": False,
                "message": "Post unliked",
                "likes_count": blog_post.likes.count(),
            }

        blog_post.likes.add(user_profile)
        return {
            "liked": True,
            "message": "Post liked",
            "likes_count": blog_post.likes.count(),
        }