from django.urls import path
from . import views

app_name="chatBot"

urlpatterns = [
    path('', views.chatBotPage, name='chatBotPage'),
]
