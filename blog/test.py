from django.test import TestCase
from users.models import User, UserProfile
from blog.models import BlogPost, Comment
from blog.api.serializers import (
    JustBlogPostSerializer,
    CommentSerializer,
    CommentGetSerializer,
    BlogPostSerializer,
    BlogPostGetSerializer,
    BlogPostLikeToggleSerializer,
)
from rest_framework.test import APIRequestFactory



class BlogPostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="authoruser",
            password="testpass123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="+1234567890"
        )

        self.blog_post = BlogPost.objects.create(
            title="Test Blog Post",
            body="This is a test blog post.",
            author=self.profile
        )

    def test_blog_post_creation(self):
        self.assertEqual(self.blog_post.title, "Test Blog Post")
        self.assertEqual(self.blog_post.author, self.profile)
        self.assertIsNotNone(self.blog_post.created_at)

    def test_blog_post_str(self):
        self.assertEqual(str(self.blog_post), "Test Blog Post")

    def test_blog_post_likes(self):
        user2 = User.objects.create_user(username="user2", password="pass123")
        profile2 = UserProfile.objects.create(
            user=user2,
            first_name="Jane",
            last_name="Smith",
            email="jane@example.com",
            phone_number="+1987654321"
        )

        self.blog_post.likes.add(profile2)

        self.assertEqual(self.blog_post.likes.count(), 1)
        self.assertTrue(self.blog_post.likes.filter(id=profile2.id).exists())


class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="commentuser",
            password="testpass123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name="Alice",
            last_name="Brown",
            email="alice@example.com",
            phone_number="+1112223333"
        )

        self.blog_post = BlogPost.objects.create(
            title="Another Post",
            body="Post body",
            author=self.profile
        )

        self.comment = Comment.objects.create(
            blog_post=self.blog_post,
            body="This is a comment",
            author=self.profile
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.blog_post, self.blog_post)
        self.assertEqual(self.comment.author, self.profile)
        self.assertEqual(self.comment.body, "This is a comment")

    def test_comment_str(self):
        expected_str = f"Comment by {self.profile.first_name} {self.profile.last_name} on {self.blog_post.title}"
        self.assertEqual(str(self.comment), expected_str)

    def test_blog_post_comment_relationship(self):
        self.assertEqual(self.blog_post.comments.count(), 1)
        self.assertEqual(self.blog_post.comments.first(), self.comment)


class BaseSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pass12345"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="+1234567890"
        )

        self.blog_post = BlogPost.objects.create(
            title="Test Post",
            body="Post body",
            author=self.profile
        )

        self.comment = Comment.objects.create(
            blog_post=self.blog_post,
            body="Test comment",
            author=self.profile
        )


class BaseSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="pass12345"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="+1234567890"
        )

        self.blog_post = BlogPost.objects.create(
            title="Test Post",
            body="Post body",
            author=self.profile
        )

        self.comment = Comment.objects.create(
            blog_post=self.blog_post,
            body="Test comment",
            author=self.profile
        )


class JustBlogPostSerializerTest(BaseSerializerTest):

    def test_just_blog_post_serializer(self):
        serializer = JustBlogPostSerializer(self.blog_post)
        data = serializer.data

        self.assertEqual(data["title"], "Test Post")
        self.assertEqual(data["body"], "Post body")
        self.assertEqual(data["author"], str(self.profile))


class CommentSerializerTest(BaseSerializerTest):

    def test_comment_serializer(self):
        serializer = CommentSerializer(self.comment)
        data = serializer.data

        self.assertEqual(data["body"], "Test comment")
        self.assertEqual(data["author"], str(self.profile))
        self.assertEqual(data["blog_post"], self.blog_post.id)

class CommentGetSerializerTest(BaseSerializerTest):

    def test_comment_get_serializer(self):
        serializer = CommentGetSerializer(self.comment)
        data = serializer.data

        self.assertEqual(data["body"], "Test comment")
        self.assertEqual(data["author"]["email"], "john@example.com")
        self.assertEqual(data["blog_post"]["title"], "Test Post")

class BlogPostSerializerTest(BaseSerializerTest):

    def test_blog_post_serializer(self):
        serializer = BlogPostSerializer(self.blog_post)
        data = serializer.data

        self.assertEqual(data["title"], "Test Post")
        self.assertEqual(len(data["comments"]), 1)
        self.assertEqual(data["comments"][0]["body"], "Test comment")


class BlogPostGetSerializerTest(BaseSerializerTest):

    def test_blog_post_get_serializer(self):
        serializer = BlogPostGetSerializer(self.blog_post)
        data = serializer.data

        self.assertEqual(data["author"]["email"], "john@example.com")
        self.assertEqual(len(data["comments"]), 1)


class BlogPostLikeToggleSerializerTest(BaseSerializerTest):

    def setUp(self):
        super().setUp()
        self.factory = APIRequestFactory()
        self.request = self.factory.post("/")
        self.request.user = self.user

    def test_like_post(self):
        serializer = BlogPostLikeToggleSerializer(
            context={
                "request": self.request,
                "blog_post": self.blog_post,
            }
        )

        result = serializer.save()

        self.assertTrue(result["liked"])
        self.assertEqual(result["likes_count"], 1)
        self.assertTrue(self.blog_post.likes.filter(id=self.profile.id).exists())

    def test_unlike_post(self):
        self.blog_post.likes.add(self.profile)

        serializer = BlogPostLikeToggleSerializer(
            context={
                "request": self.request,
                "blog_post": self.blog_post,
            }
        )

        result = serializer.save()

        self.assertFalse(result["liked"])
        self.assertEqual(result["likes_count"], 0)
        self.assertFalse(self.blog_post.likes.filter(id=self.profile.id).exists())
