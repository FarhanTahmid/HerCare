from django.db import models

# Create your models here.

class ThreadsWithTimeStamps(models.Model):
    thread_id=models.CharField(null=False,blank=False,primary_key=True,max_length=200)
    timestamp=models.DateTimeField(null=False,blank=False,max_length=100)
    
    class Meta:
        verbose_name="Conversation Threads and Timestamps"
    
    def __str__(self) -> str:
        return str(self.thread_id)
