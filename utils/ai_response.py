import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage, AssistantMessage
from azure.core.credentials import AzureKeyCredential

endpoint = "https://models.github.ai/inference"
model = "gpt-4o-mini"
from dotenv import load_dotenv
load_dotenv()
token = os.environ["sir_token"]

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def get_completion(user_message, system_message="You are a helpful assistant.", history=None):
    """
    Get a completion from the AI model with optional history.
    """
    messages = [SystemMessage(system_message)]
    
    if history:
        for msg in history:
            if msg.role == 'user':
                messages.append(UserMessage(msg.content))
            elif msg.role == 'assistant':
                messages.append(AssistantMessage(msg.content))
                
    messages.append(UserMessage(user_message))

    response = client.complete(
        messages=messages,
        model=model
    )
    return response.choices[0].message.content