from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from blog.models import BlogPost, Comment
from .serializers import BlogPostGetSerializer, BlogPostLikeToggleSerializer, BlogPostSerializer, CommentGetSerializer, CommentSerializer
from users.models import UserProfile
from django.shortcuts import get_object_or_404


class BlogPostLikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BlogPostLikeToggleSerializer


    def post(self, request, pk):
        blog_post = get_object_or_404(BlogPost, pk=pk)

        serializer = BlogPostLikeToggleSerializer(
            context={
                "request": request,
                "blog_post": blog_post,
            }
        )

        data = serializer.save()
        return Response(data, status=200)

class BlogPostListAPIView(generics.ListAPIView):
    serializer_class = BlogPostGetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return (
            BlogPost.objects
            .select_related("author")
            .prefetch_related("comments", "likes")
            .order_by("-created_at")
        )


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentGetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BlogPostCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = BlogPostSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            author = UserProfile.objects.get(user=request.user)
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get all comments or create a new one
class CommentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer


    def post(self, request):
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            author = UserProfile.objects.get(user=request.user)
            serializer.save(author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
