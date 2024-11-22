from django.urls import path
from . import views
from .views import *

app_name="api"

urlpatterns = [
    path('bot-response/',views.bot_response,name='bot_response'),
    path('download-user-convo/',GetUserChatData.as_view(),name='user_conversation'),
]
