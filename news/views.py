from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication


from .models import *
from .serializers import *
from .permissions import IsAuthorPermission


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.author)

    def get_queryset(self):
        queryset = self.queryset
        print(self.request.query_params)
        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author__user__username=author)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)
        return queryset


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):

        return self.queryset.filter(news_id=self.kwargs['news_id'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        news=get_object_or_404(News, id=self.kwargs['news_id']))


class CommentRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]


class NewsLikeView(APIView):
    def get(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        try:
            like = NewsLikeView.objects.create(news=news, author=request.author)
        except IntegrityError:
            like = NewsLikeView.objects.filter(news=news, author=request.author).delete()
            data = {f"Лайк для {news_id} твита убрал пользователь {request.author.user.username}"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            if DislikeNews.objects.filter(news=news, author=request.author):
                dislike = DislikeNews.objects.get(news=news, author=request.author).delete()
                data = {f"Был убран дизлайк с твита {news_id} и вместо неё поставлен лайк пользователем"
                        f" {request.author.user.username}"}
                return Response(data, status=status.HTTP_201_CREATED)
            data = {'message': f"лайк твиту {news_id} поставил пользователь {request.author.user.username}"}
            return Response(data, status=status.HTTP_201_CREATED)


class NewsDislikeView(APIView):
    def get(self, request, news_id):
        news = get_object_or_404(News, id=news_id)
        try:
            like = NewsDislikeView.objects.create(news=news, user=request.author)
        except IntegrityError:
            like = NewsDislikeView.objects.filter(news=news, user=request.author).delete()
            data = {'Errors': f"дизлайк {news_id} был убран пользователем {request.author.user.username}"}
            return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            if DislikeNews.objects.filter(news=news, user=request.author):
                like = DislikeNews.objects.get(news=news, user=request.author).delete()
                data = {f"Был убран лайк с новости {news_id} и вместо неё поставлен дизлайк пользователем"
                        f" {request.author.user.username}"}
                return Response(data, status=status.HTTP_201_CREATED)
            data = {f"дизлайк для новости {news_id} поставил пользователь {request.author.user.username}"}
            return Response(data, status=status.HTTP_201_CREATED)
