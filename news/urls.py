from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')
# router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('news/<int:news_id>/comment/', views.CommentListCreateAPIView.as_view()),
    path('news/<int:news_id>/comment/<int:pk>/', views.CommentRetrieveDestroyAPIView.as_view()),
    path('news/<int:news_id>/like/', views.NewsLikeView.as_view()),
    path('news/<int:news_id>/dislike/', views.NewsDislikeView.as_view()),


]
