import os
from openai import OpenAI
from chatBot.context_generation import ContextGeneration

class Chatbot:
    
    client=OpenAI()
    
    def __init__(self,thread_id,assistant_id):
        self.thread_id = thread_id
        self.assistant_id=assistant_id
    
    def showThreadID(self):
        print(f"Generated Thread ID from helper is: {self.thread_id}")
    
    def generateNormalGPTMessages(self,user_message):
        try:
            generate_message=self.client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {"role": "system", "content": "Be good"},
                    {"role": "user", "content": f"{user_message}"}
                ]
            )
            return generate_message.choices[0].message.content
        except Exception as e:
            print(f"Can not generate normal GPT messages because of: {e}")
            return None
    
    def createMessageToThread(self,user_message):
        posts_title,posts_text,post_comments=ContextGeneration.generateContext(message=user_message)
        print(posts_title,posts_text,post_comments)
        
        user_message_with_context=user_message+f' cntxt- Some relevant reddit posts_list,post_texts_list, post_comments list related to the user text are given here: Posts:{posts_title}, Text in the Posts:{posts_text}, Corresponding comments with the post: {post_comments}'
        try:
            if len(user_message_with_context)<254000:
                message=self.client.beta.threads.messages.create(
                    thread_id=self.thread_id,
                    role='user',
                    content=user_message_with_context
                )
                return True
            else:
                message=self.client.beta.threads.messages.create(
                    thread_id=self.thread_id,
                    role='user',
                    content=user_message
                )
                return True
        except Exception as e:
            print(f"Can not create message to thread because of: {e}")
            return False
    
    def createRunAndGenerateMessage(self):
        try:
            run=self.client.beta.threads.runs.create_and_poll(thread_id=self.thread_id,assistant_id=self.assistant_id)
            if(run.status=='completed'):
                response=self.client.beta.threads.messages.list(thread_id=self.thread_id)
                bot_message=response.data[0].content[0].text.value
                return bot_message
            else:
                print(f"Run Status: {run.status}")
                return None
        except Exception as e:
            print(f"Error creating run for {e}")
            return None
    
    def generateAssistantMessage(self,user_message):
        try:
            if(self.createMessageToThread(user_message=user_message)):
                bot_message=self.createRunAndGenerateMessage()
                if bot_message:
                    return bot_message
                else:
                    return self.generateNormalGPTMessages(user_message=user_message)
        except Exception as e:
            print(f"Error generating assistant message for {e}")
            return None
