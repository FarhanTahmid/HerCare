from django.shortcuts import render
from openai import OpenAI
import datetime
import os
from .helpers import HelperClass
from .bot import Chatbot
from .models import *
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.cache import cache

# Create your views here.

def chatBotPage(request):
    # record the timestamp of page loading at first
    timestamp=datetime.datetime.now()
    print(f"The current timestamp is {str(timestamp)}")
    
    # now we initialize all the openAI functions
    client=OpenAI()
    assistant_id=os.environ.get('ASSISTANT_ID')
    # create new thread with helper class
    new_thread_id=HelperClass.createNewThread(openAI_client=client)
    
    if new_thread_id is not None:
        print(f"New thread id is {new_thread_id}")
        
        # Store this thread and timestamp in database to crosscheck later
        try:
            new_conversation=ThreadsWithTimeStamps.objects.create(
                thread_id=new_thread_id,timestamp=timestamp
            )
            new_conversation.save()
            print(f"New conversation saved in database with id {new_conversation.thread_id}")
        except Exception as e:
            print(f"Error saving conversation in database: {str(e)}")
            
        # initialize chatbot now
        chatbot=Chatbot(new_thread_id,assistant_id)
        print(f"Object in Bot view is: {chatbot.thread_id}")
        chatbot.showThreadID()
        
    else:
        # show error
        print("Can not start a new conversation!")    
    
    # get API URL for the application to pass it in context
    api_url = os.environ.get('API_URL')
    context={
        'api_url':api_url,
        'thread_id':chatbot.thread_id,
        'assistant_id':assistant_id,
    }
    return render(request, 'chatbot.html',context=context)

