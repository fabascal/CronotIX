import sys
import os
from flask import jsonify, current_app, session
from flask_login import current_user
from website import db
import os
import dotenv
dotenv.load_dotenv()
import json
import time
import importlib
from .exceptions import FunctionNotFoundError

from openai import OpenAI, AsyncOpenAI

OpenAI.api_key = os.getenv('OPENAI_API_KEY')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')

key = os.getenv('OPENAI_API_KEY')

def import_client_functions(client_id):
    # Asegúrate de que el directorio raíz del proyecto esté en sys.path
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if root_path not in sys.path:
        sys.path.append(root_path)
    
    module_path = f"website.home.controller.functions.{client_id}.functions"
    try:
        module = importlib.import_module(module_path)
        current_app.logger.info(f"Importing functions for client {module_path}")
        return module
    except ImportError as e:
        current_app.logger.error(f"No se pudo importar el módulo: {e}")
        print(f"No se pudo importar el módulo: {e}")
        return None

class AssistantController:
    def __init__(self, client_id, thread_id=None):
        self.client = OpenAI()
        self.client_id = client_id
        self.Functions = import_client_functions(client_id).Functions
        self.message = None
        self.run = None
        self.thread_id = thread_id if thread_id is not None else self.create_thread()
        
    def create_assistant(self):
        assistant = self.client.beta.assistants.create(
               name="Random Assistant",
               instructions="Format your responses in markdown.",
               model="gpt-4-1106-preview",
            #    tools=[{"type": "function", "function": Functions.get_random_digit_JSON},
            #           {"type": "function", "function": Functions.get_random_letters_JSON}]
            )
        return assistant.id


    def create_thread(self):
        thread = self.client.beta.threads.create(
            tool_resources={
                "file_search": {
                "vector_store_ids": ["vs_3jgzYpQah0qWqfa8X6OYpX7g"]
                }
            }
        )
        current_app.logger.info(f"Thread created: {thread.id}")
        return thread.id

    def sendMessage(self, message:str):
        print(f'\nSending message to assistant: {message}')
        self.message = self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role='user',
            content=message
        )
        self.run = self.client.beta.threads.runs.create_and_poll(thread_id=self.thread_id, assistant_id=ASSISTANT_ID)
        return self.waitThread()

    def waitThread(self):
        while self.run.status in ['queued', 'in_progress']:
            self.run = self.client.beta.threads.runs.retrieve(thread_id=self.thread_id, run_id=self.run.id)
            current_app.logger.info(f"Run status: {self.run.status}")
            time.sleep(1)
        if self.run.status == 'requires_action':
            tool_outputs = self.handle_required_actions()
            self.run = self.client.beta.threads.runs.submit_tool_outputs(thread_id=self.thread_id, run_id=self.run.id, tool_outputs=tool_outputs)
            return self.waitThread()
        else:
            #new_messages = self.client.beta.threads.messages.list(thread_id=self.thread_id, order="asc")
            # new_messages = self.client.beta.threads.messages.list(thread_id=self.thread_id, order="asc", after=self.message.id)
            new_messages = self.client.beta.threads.messages.list(thread_id=self.thread_id, run_id=self.run.id)
            return new_messages

    def handle_required_actions(self):
        try :
            tool_outputs = []
            for tool_call in self.run.required_action.submit_tool_outputs.tool_calls:
                tool_call_id = tool_call.id
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                current_app.logger.info(f"Assistant requested {name}: {arguments}")
                output = getattr(self.Functions, name)(**arguments)
                tool_outputs.append({"tool_call_id": tool_call_id, "output": json.dumps(output)})
            return tool_outputs
        except FunctionNotFoundError as e:
            current_app.logger.error(str(e))
            return {'error': str(e)}