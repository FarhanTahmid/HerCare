from django.conf import settings
import requests

class OpenSourceBot():
    def __init__(self, name, version):
        self.name = name
        self.version = version
    
    def deepseekResponse(self, prompt):
        API_KEY = settings.DEEPSEEK_API_KEY
        
        url = "https://api.deepseek.com/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        data = {
            "model": "deepseek-reasoner",  # 'deepseek-reasoner' for R1 model or 'deepseek-chat' for V3 model
            "messages": [
                {"role": "user", "content": {prompt}}
            ],
            "stream": False  # Disable streaming
        }
        try:
            api_response = requests.post(
                url=url,
                headers=headers,
                json=data
            )
            
            if api_response.status_code != 200:
                api_response.raise_for_status()
            else:
                result = api_response.json()
                response_text = result['choices'][0]['message']['content']
                print(response_text)
        except requests.exceptions.RequestException as e:
            response_text = f"Error: {str(e)}"
            print(response_text)