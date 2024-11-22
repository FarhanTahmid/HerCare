from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from chatBot.bot import Chatbot
import pickle
from django.core.cache import cache
from chatBot.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from openai import OpenAI
from django.http import HttpResponse
import csv
import datetime

# Create your views here.
@csrf_exempt
def bot_response(request):
    # get post request from APIs
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            user_message=data.get("message","")
            print(f"User Message:{user_message}")
            
            thread_id=data.get("thread_id","")
            assistant_id=data.get("assistant_id","")
            
            chatbot=Chatbot(assistant_id=assistant_id,thread_id=thread_id)
            print(f"Object in API view is {chatbot.thread_id}")
            
            # now generate the bot message here and send it as response.
            bot_message=chatbot.generateAssistantMessage(user_message=user_message)

            if bot_message:
                return JsonResponse({
                    'bot_message':bot_message,
                },status=200)
            else:
                return JsonResponse({"error": "Error fetching message"}, status=400)

            
        except Exception as e:
            print(f"Error fetching message:{e}")
            return JsonResponse({"error": "Error fetching message"}, status=400)
    else:    
        return JsonResponse({"error": "Invalid request method."}, status=405)




class GetUserChatData(APIView):
    client=OpenAI()
    
    @permission_classes([IsAuthenticated])
    def get(self,request):
        if request.user.is_authenticated:
            # get all the threads stored in the database
            try:
                get_all_threads=ThreadsWithTimeStamps.objects.filter().all().order_by('timestamp')
            except Exception as e:
                print(f"Error fetching threads:{e}")
                return False
            
            data = []  # To store rows for the CSV

            try:
                for thread in get_all_threads:
                    print(thread.thread_id)
                    thread_id=thread.thread_id
                    timestamp=thread.timestamp
                    
                    # make list for messages
                    user_message_list=[]
                    actual_user_message_list=[]
                    assistant_message_list=[]
                    
                    thread_messages=GetUserChatData.client.beta.threads.messages.list(thread_id=thread.thread_id)
                    for message in (thread_messages.data):
                        if(message.role=='user'):
                            user_message_list.append(message.content[0].text.value)
                        elif(message.role=='assistant'):
                            assistant_message_list.append(message.content[0].text.value)
                    for message in user_message_list:
                        actual_user_message_list.append(message.split('cntxt-')[0])
                    
                    # Combine user and assistant messages into rows
                    for user_msg, assistant_msg in zip(actual_user_message_list[::-1], assistant_message_list[::-1]):
                        data.append({
                            "timestamp": timestamp,
                            "thread_id": thread_id,
                            "user_message": user_msg,
                            "chatbot_response": assistant_msg,
                        })
                    
                response = HttpResponse(content_type='text/csv')
                custom_filename = f"User Conversations_HerCare_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                response['Content-Disposition'] = f'attachment; filename="{custom_filename}"'

                writer = csv.DictWriter(response, fieldnames=["timestamp", "thread_id", "user_message", "chatbot_response"])
                writer.writeheader()
                writer.writerows(data)
                        
                return response
            except Exception as e:
                print(f"Error generating CSV file:{e}")
                return JsonResponse({"error": "Something went wrong while generating the CSV file."}, status=405)
        else:
            return JsonResponse({"error": "You do not have permission to view this!."}, status=405)

        