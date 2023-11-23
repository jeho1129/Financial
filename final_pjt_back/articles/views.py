from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Article, Comment
from .serializers import ArticleSerializer, ArticleListSerializer, CommentSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    if request.method == 'GET':
        serializer = ArticleListSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        if request.user == article.user:
            serializer = ArticleSerializer(article, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        
    elif request.method == 'DELETE':
        if request.user == article.user or request.user.is_staff:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(article=article, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def comment_detail(request, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'PUT':
        if request.user == comment.user:
            serializer = CommentSerializer(comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        if request.user == comment.user or request.user.is_staff:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)