from django.db import models
from django.utils import timezone
# Create your models here.

class Questions(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.pk

class Response(models.Model):
    PROVIDER_CHOICES = [
        ('OPENAI', 'OpenAI GPT o1'),
        ('LLAMA', 'Llama'),
        ('HerCare', 'HerCare'),
    ]
    question = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='responses')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    text = models.TextField()
    response_time = models.FloatField(help_text="Response time in seconds")
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.provider} response to {self.question}"