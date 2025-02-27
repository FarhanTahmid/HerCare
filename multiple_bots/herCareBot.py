from openai import OpenAI
import os
import time
from chatBot.bot import Chatbot
import requests

class HerCareBot:
    
    @staticmethod
    def getResponse(thread_id,assistant_id,question_text):
        start_time = time.time()
        try:
            if thread_id is not None:
                chatbot=Chatbot(assistant_id=assistant_id,thread_id=thread_id)
                bot_message=chatbot.generateAssistantMessage(user_message=question_text)
                elapsed_time = time.time() - start_time
                
                return bot_message, elapsed_time
        except requests.exceptions.RequestException as e:
            return f"Error: Could not get response from OpenAI. {str(e)}", time.time() - start_time
