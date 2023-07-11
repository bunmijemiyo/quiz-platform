from django.contrib import admin
from django.urls import path, re_path, include
from .views import (create_question, display_questions, update_question,
                    take_test, QuestionCreateView, QuestionAPIView,
                    AnswerChoiceAPIView, ChoiceDetails, QuestionDetails,
                    ChoiceCreateView, QuestionUpdateView, AnswerChoiceUpdateView,
                    QuestionUpdateViews)
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # re_path("viewset/(?P<pk>\d+)?", include(router.urls)),
    # path('createtest/', create_test),
    path('api/create_question/', QuestionCreateView.as_view(), name='createApiQuest'),
    path('api/questions/', QuestionAPIView.as_view(), name='apiQuestions'),
    path('api/questions/<int:id>/', QuestionDetails.as_view(), name='apiQuestion'),
    path('api/choice/', AnswerChoiceAPIView.as_view(), name='apiChoice'),
    path('api/choice/<int:quest>/', ChoiceDetails.as_view(), name='apiChoiceDetail'),
    path('api/create_choice/', ChoiceCreateView.as_view(), name='apiCreateChoice'),
    path('api/update_question/<int:question_id>/', QuestionUpdateView.as_view(), name='apiUpdateQuest'),
    path('api/update_choice/<int:choice_id>/', AnswerChoiceUpdateView.as_view(), name='apiUpdateChoice'),
    path('api/update_quest/<int:question_id>/', QuestionUpdateViews.as_view(), name='question-update'),
    # path('article/', ArticleAPIView.as_view()),
    # path('generic/article/', GenericAPIView.as_view()),
    # re_path('generic/article/(?P<id>\d+)?', GenericAPIView.as_view()),
    # path('detail/<int:pk>/', article_detail),
    # path('detail/<int:id>/', ArticleDetails.as_view()),
    path('create', create_question, name='create'),
    path('display', display_questions, name='display'),
    path('take_test/', take_test, name='takeTest'),
    path('update_test/<int:question_id>/', update_question, name='updateTest'),

]
