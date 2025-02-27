import asyncio
import concurrent.futures
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from .models import Questions, Response
from .openaiBot import OpenAIBot
from .llamaBot import LlamaBot
# from .services.custom_service import CustomModelService

class IndexView(View):
    """View for the main page"""
    
    def get(self, request):
        """Handle GET request to display the question form"""
        return render(request, 'index.html')

class AskQuestionView(View):
    """View for handling question submission and displaying results"""
    
    def get(self, request):
        """Handle GET request - redirect to index"""
        return redirect('multiple_bots:index')
    
    def post(self, request):
        """Handle POST request to process a question and get AI responses"""
        question_text = request.POST.get('question', '')
        
        if not question_text:
            return JsonResponse({
                'error': 'Question cannot be empty'
            }, status=400)
        
        # Create a new question in the database
        question = Questions.objects.create(text=question_text)
        
        # Get responses from all AI models in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                'OPENAI': executor.submit(OpenAIBot.get_response, question_text),
                'LLAMA': executor.submit(LlamaBot.get_response, question_text),
                # 'CUSTOM': executor.submit(CustomModelService.get_response, question_text),
            }
            
            responses = {}
            for provider, future in futures.items():
                try:
                    response_text, response_time = future.result()
                    
                    # Save response to database
                    Response.objects.create(
                        question=question,
                        provider=provider,
                        text=response_text,
                        response_time=response_time
                    )
                    
                    responses[provider] = {
                        'text': response_text,
                        'time': round(response_time, 2)
                    }
                except Exception as e:
                    responses[provider] = {
                        'text': f"Error: {str(e)}",
                        'time': 0
                    }
        
        # Render the results page with all responses
        return render(request, 'results.html', {
            'question': question,
            'responses': responses
        })

@method_decorator(csrf_exempt, name='dispatch')
class ApiAskQuestionView(View):
    """API view for handling question submission and returning JSON responses"""
    
    def post(self, request):
        """Handle POST request to process a question and get AI responses as JSON"""
        import json
        
        try:
            data = json.loads(request.body)
            question_text = data.get('question', '')
            
            if not question_text:
                return JsonResponse({
                    'error': 'Question cannot be empty'
                }, status=400)
            
            # Create a new question in the database
            question = Questions.objects.create(text=question_text)
            
            # Get responses from all AI models in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = {
                    'OPENAI': executor.submit(OpenAIBot.get_response, question_text),
                    'LLAMA': executor.submit(LlamaBot.get_response, question_text),
                    # 'CUSTOM': executor.submit(CustomModelService.get_response, question_text),
                }
                
                responses = {}
                for provider, future in futures.items():
                    try:
                        response_text, response_time = future.result()
                        
                        # Save response to database
                        Response.objects.create(
                            question=question,
                            provider=provider,
                            text=response_text,
                            response_time=response_time
                        )
                        
                        responses[provider] = {
                            'text': response_text,
                            'time': round(response_time, 2)
                        }
                    except Exception as e:
                        responses[provider] = {
                            'text': f"Error: {str(e)}",
                            'time': 0
                        }
            
            return JsonResponse({
                'question_id': question.pk,
                'question_text': question.text,
                'responses': responses
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON in request body'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': f'Server error: {str(e)}'
            }, status=500)