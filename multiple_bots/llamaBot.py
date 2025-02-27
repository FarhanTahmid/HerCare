import time
import requests
from django.conf import settings
from openai import OpenAI

class LlamaBot:
    client = OpenAI(api_key=settings.LLAMA_API_KEY,base_url="https://api.llama-api.com")
    
    @staticmethod
    def get_response(question_text):
        """
        Gets a response from Llama API
        
        Args:
            question_text (str): The question to send to the API
            
        Returns:
            tuple: (response_text, response_time_in_seconds)
        """
        start_time = time.time()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.LLAMA_API_KEY}"
        }
        
        data = {
            "prompt": question_text,
            "max_tokens": 500,
            # Add other parameters specific to Llama API
        }
        
        try:
            response = LlamaBot.client.chat.completions.create(
                model="llama3.1-70b",
                messages=[
                    {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
                    {"role": "user", "content": "I love you."}
                ],
                tools = [
                {
                    'type': 'function',
                    'function':
                        {'name': 'information_extraction',
                        'description': 'Extracts the relevant information from the user message.',
                        'parameters': {
                            'type': 'object',
                            'properties': {
                                'sentiment': {'title': 'sentiment', 'type': 'string', 'description': 'the sentiment encountered in the passage'},
                                'aggressiveness': {'title': 'aggressiveness', 'type': 'integer', 'description': 'a 0-10 score of how aggressive the passage is'},
                                'language': {'title': 'language', 'type': 'string', 'description': 'the language of the passage'},
                            }, 'required': []
                        }
                    }
                }
                ]
            )
            response_text = response.choices[0].message.function_call
            elapsed_time = time.time() - start_time
            
            return response_text, elapsed_time
            
        except requests.exceptions.RequestException as e:
            # Log the error (in a production app)
            # logger.error(f"Error calling Llama API: {str(e)}")
            return f"Error: Could not get response from Llama. {str(e)}", time.time() - start_time