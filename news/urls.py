from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('news', views.NewsViewSet, basename='news')
router.register('statuses', views.StatusViewSet, basename='statuses')
# router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('news/<int:news_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('news/<int:news_id>/comments/<int:pk>/', views.CommentRetrieveDestroyAPIView.as_view()),
    path('news/<int:news_id>/<str:slug>/', views.NewsPostStatus.as_view()),
    path('news/<int:news_id>/comments/<int:comment_id>/<str:slug>/', views.CommentPostStatus.as_view()),
]
