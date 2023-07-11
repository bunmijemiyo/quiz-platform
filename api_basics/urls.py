from django.contrib import admin
from django.urls import path, re_path, include
from .views import article_list, article_detail, ArticleAPIView, ArticleDetails, GenericAPIView, ArticleViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("article", ArticleViewSet, basename="article")

urlpatterns = [
    re_path("viewset/(?P<pk>\d+)?", include(router.urls)),
    # path('article/', article_list),
    path('article/', ArticleAPIView.as_view()),
    # path('generic/article/', GenericAPIView.as_view()),
    re_path('generic/article/(?P<id>\d+)?', GenericAPIView.as_view()),
    # path('detail/<int:pk>/', article_detail),
    path('detail/<int:id>/', ArticleDetails.as_view()),

]
