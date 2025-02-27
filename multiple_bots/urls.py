from django.urls import path
from . import views

app_name = 'multiple_bots'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('ask/', views.AskQuestionView.as_view(), name='ask_question'),
    path('api/ask/', views.ApiAskQuestionView.as_view(), name='api_ask_question'),
]