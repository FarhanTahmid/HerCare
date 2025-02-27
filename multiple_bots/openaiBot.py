import time
import requests
from django.conf import settings

class OpenAIBot:
    """Service to interact with OpenAI GPT API"""
    
    @staticmethod
    def get_response(question_text):
        """
        Gets a response from OpenAI API
        
        Args:
            question_text (str): The question to send to the API
            
        Returns:
            tuple: (response_text, response_time_in_seconds)
        """
        start_time = time.time()
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
        }
        
        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question_text}
            ],
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                settings.OPENAI_API_ENDPOINT,
                headers=headers,
                json=data,
                timeout=settings.API_TIMEOUT
            )
            
            response.raise_for_status()
            response_data = response.json()
            
            response_text = response_data['choices'][0]['message']['content']
            elapsed_time = time.time() - start_time
            
            return response_text, elapsed_time
            
        except requests.exceptions.RequestException as e:
            # Log the error (in a production app)
            # logger.error(f"Error calling OpenAI API: {str(e)}")
            return f"Error: Could not get response from OpenAI. {str(e)}", time.time() - start_time