from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .models import *
from .serializers import *
from .permissions import IsAuthorPermission


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)

    def get_queryset(self):
        queryset = self.queryset
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
        serializer.save(author=self.request.user.author,
                        news=get_object_or_404(News, id=self.kwargs['news_id']))


class CommentRetrieveDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthorPermission, ]


class NewsPostStatus(APIView):
    model = NewsStatus
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, news_id, slug):
        news = get_object_or_404(News, id=news_id)
        status = get_object_or_404(Status, slug=slug)
        try:
            self.model.objects.create(
                news=news,
                author=request.user.author,
                status=status
            )
        except IntegrityError:
            return Response({'error': 'You already added status'})
        else:
            return Response({'message': 'Status added'})


class CommentPostStatus(APIView):
    model = CommentStatus
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get(self, request, news_id, comment_id, slug):
        comment = get_object_or_404(Comment, id=comment_id, news__id=news_id)
        status = get_object_or_404(Status, slug=slug)
        try:
            self.model.objects.create(
                comment=comment,
                author=request.user.author,
                status=status
            )
        except IntegrityError:
            return Response({'error': 'You already added status'})
        else:
            return Response({'message': 'Status added'})


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser, ]
