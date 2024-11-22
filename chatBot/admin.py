from django.contrib import admin
from . models import *
# Register your models here.

@admin.register(ThreadsWithTimeStamps)
class ThreadsWithTimeStampsAdmin(admin.ModelAdmin):
    list_display=[
        'thread_id','timestamp'
    ]