class HelperClass:
    
    def createNewThread(openAI_client):
        # Create a new thread that will run the openAI_client
        try:
            new_thread=openAI_client.beta.threads.create()
            return new_thread.id
        except Exception as e:
            print(f"Error creating new thread: {e}")
            return None