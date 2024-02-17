import uuid
from datetime import timedelta, datetime, timezone

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from feed.decorators import login_decorator
from feed.models import Post, Comment, FeedUser, Token
from feed.serializers import PostSerializer, CommentSerializer, FeedUserSerializer


# Create your views here.

@api_view(['POST'])
def login(request):
    if FeedUser.objects.filter(name=request.data['name']).exists():
        user = FeedUser.objects.get(name=request.data['name'])
        if user.password == request.data['password']:
            token, created = Token.objects.get_or_create(user=user, defaults=dict(expires_on=datetime.now()))
            if created:
                token.token = str(uuid.uuid4())
            token.expires_on = datetime.now() + timedelta(14)
            token.save()
            return Response({'success': True, 'token': token.token})
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register(request):
    if FeedUser.objects.filter(name=request.data['name']).exists():
        return Response({'message': 'User already exists'}, status=400)
    user = FeedUser.objects.create(
        name=request.data.get('name'),
        password=request.data.get('password')
    )
    serializer = FeedUserSerializer(user).data
    return Response(serializer)


@api_view(['GET'])
def get_post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True).data
    return Response(serializer)


@api_view(['POST'])
@login_decorator
def add_post(request):
    if not isinstance(request.data, dict):
        return Response({'error': 'Not a dict'}, status=400)
    if Post.objects.filter(title=request.data['title']).exists():
        return Response({'error': 'Post with title exists'}, status=400)
    if 'title' not in request.data:
        return Response({'error': 'Post must have title'}, status=400)
    if 'content' not in request.data:
        return Response({'error': 'Post must have content'}, status=400)
    post = Post.objects.create(
        title=request.data['title'],
        content=request.data['content'],
        created_by=request.user
    )
    post_data = PostSerializer(post).data
    return Response(post_data)


@api_view(['POST'])
@login_decorator
def add_comment(request):
    if not isinstance(request.data, dict):
        return Response({'error': 'Not a dict'}, status=400)
    if 'message' not in request.data:
        return Response({'error': 'Comment must have message'}, status=400)
    if 'post_id' not in request.data:
        return Response({'error': 'Comment must have post_id'}, status=400)
    comment = Comment.objects.create(
        message=request.data['message'],
        post_id=request.data['post_id'],
        created_by=request.user
    )
    comment_data = CommentSerializer(comment).data
    return Response(comment_data)


@api_view(['GET'])
def get_comments_for_post(request, post_id):
    comments = Comment.objects.filter(post_id=post_id)
    comment_data = CommentSerializer(comments, many=True).data
    return Response(comment_data)


@api_view(['GET'])
@login_decorator
def get_comments_for_user(request):
    user = FeedUser.objects.get(id=request.user.id)
    comments = user.comment_set.all()
    comment_data = CommentSerializer(comments, many=True).data
    return Response(comment_data)


@api_view(['POST'])
@login_decorator
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.liked_by.add(request.user)
    return Response(post.liked_by.count())
