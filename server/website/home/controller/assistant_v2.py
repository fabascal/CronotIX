import sys
import os
from openai import OpenAI
from flask import current_app
from website import db
from website.home.models import Assistants, AssistantsVector, AssistantsFiles


KEY = os.getenv('OPENAI_API_KEY')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')


class AssistantController:
    def __init__(self, client_id=None, thread_id=None, assistant_id=None):
        self.client = OpenAI()
        self.client.api_key = KEY
        current_app.logger.info(f'llave {KEY}')
        self.assistant_id = assistant_id
        self.message = None
        self.run = None
        self.thread_id = thread_id if thread_id is not None else self.create_thread()
        
    def create_assistant(self, data):
        description = """
            Eres un 'asistente de política' para 'Ener' quien responde a los empleados de manera eficiente con respuestas precisas sobre las políticas de la empresa para esto tendrás que buscar en tus archivos adjuntos, esta información la encontrarás en los manuales.
        """
        
        Instruction = """
            No entable ninguna otra conversación que no esté relacionada con las políticas de 'ener' o información relativa a la empresa, en caso de que el usuario esté haciendo preguntas ajenas a ella entonces discúlpese de la conversación respondiendo lo siguiente: 'Me disculpo pero como asistente virtual, solo puedo guiarte con respecto a las políticas y la información específica de la empresa.'
        """
        assistant = self.client.beta.assistants.create(
            name=data['name'],
            description=data['description'],
            instructions=data['instructions'],
            model="gpt-4-turbo",
            tools=[{"type":"file_search"}],
            temperature=0.2,
        )
        current_app.logger.info(f"Assistant created: {assistant}")
        return assistant.id
    
    def run_assistant(self, data, assistant_id = None, vector=None):
        current_app.logger.info(f"Data: {data}")
        #creamos un vector para guardar los archivos
        
        current_app.logger.info(f"Vector in run_assitant: {vector}")
        current_app.logger.info(f"Vector in run_assitant: {vector.vector}")
        #actualizamos el vector con nuevos archivos
        if vector.vector:
            assistant = Assistants.query.filter_by(id=assistant_id).first()
            current_app.logger.info(f"Vector: {vector}")
            file_path = data['file_path']
            file_stream = [open(path, "rb") for path in file_path]
            file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector.vector,
                files = file_stream
            )
            return assistant.id_openai, vector.vector, file_batch
        #creamos vector y cargamos archivos
        else:
            vector_store = self.client.beta.vector_stores.create(name=data['name'])            
            file_path = data['file_path']
            file_stream = [open(path, "rb") for path in file_path]
            file_batch = self.client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id,
                files = file_stream
            )
            assistant = self.client.beta.assistants.update(
                assistant_id=data['assistant_id'],
                tool_resources={
                    "file_search": {
                        "vector_store_ids": [vector_store.id]
                    }
                },
            )
            return assistant, vector_store.id, file_batch
        
        
    def create_thread(self):
        thread = self.client.beta.threads.create()
        current_app.logger.info(f"Thread created: {thread}")
        return thread.id
    
    def sendMessage(self,data):
        current_app.logger.info(f"Data: {data}")
        message = self.client.beta.threads.messages.create(
            thread_id=data['thread_id'],
            role='user',
            content=data['message'],
        )
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=data['thread_id'],
            assistant_id=data['assistant_id'],
        )
        messages = list(self.client.beta.threads.messages.list(thread_id=data['thread_id'], run_id=run.id))
        current_app.logger.info(f"Messages: {messages}")
        if messages and messages[0].content:
            # Si la lista de mensajes y el contenido del primer mensaje no están vacíos
            current_app.logger.info(f"Messages: {messages}")
            message_content = messages[0].content[0].text  # Asegúrate de acceder a 'value' también
        else:
            # Manejar el caso donde no hay contenido o está vacío
            current_app.logger.warning("No hay contenido en el mensaje o la lista de mensajes está vacía")
            message_content = "Ups algo salio mal, por favor intenta de nuevo."
        return message_content
    
    def readFiles(self, assistant_id):
        vector = AssistantsVector.query.filter_by(assistant_id=assistant_id).first()
        vector_store_files = self.client.beta.vector_stores.files.list(
            vector_store_id=vector.vector,
            )
        
        for file in vector_store_files:
            file_openai = self.client.files.retrieve(file.id)
            file_obj = AssistantsFiles.query.filter_by(name=file_openai.filename).first()
            file_obj.file_id = file_openai.id
            db.session.commit()
        return vector_store_files
    
    def deleteFile(self, vectore_id, file_id):
        
        deleted_vector_store_file = self.client.beta.vector_stores.files.delete(
            vector_store_id=vectore_id,
            file_id=file_id
        )
        self.client.files.delete(file_id)

        return deleted_vector_store_file