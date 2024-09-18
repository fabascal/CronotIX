import os
from flask import render_template, current_app, flash, request, jsonify, url_for, session, redirect, send_file
from flask_login import login_required, current_user
from website.home import blueprint
from website.home.forms import AssistantForm, CounterAssistantForm, AssistantHandlerForm, ModelsForm, AssistantFileForm
from website.home.models import AssistantsModels, Assistants, AssistantsVersion, AssistantsApiKey, AssistantsFiles, AssistantsVector
import time 
from datetime import datetime
from website.home.models import Assistants
#from website.home.controller.assistant import AssistantController
from website.home.controller.assistant_v2 import AssistantController
from website.auth.api_key import require_api_key
from website import csrf, db
import secrets
import json
import traceback
from website.log import logging_decorator


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')

@blueprint.route('/asistentes', methods=['GET'])
@login_required
def assistants():
    assistants = Assistants.query.filter_by(user_id=current_user.id).all()
    for assistant in assistants:
        print(f'{assistant}')
    return render_template('home/assistants.html', segment='assistants-list', assistants=assistants)

@blueprint.route('/asistentes/form', methods=['GET', 'POST'])
@blueprint.route('/asistentes/form/<assistant_id>', methods=['GET', 'POST'])
@login_required
def handler_assistant_form(assistant_id=None):   
    models = AssistantsModels.query.all()
    model_choices = [(model.id, model.name) for model in models]
    version = AssistantsVersion.query.all()
    version_choices = [(version.id, version.name) for version in version]

    if assistant_id:
        assistant = Assistants.query.filter_by(id=assistant_id).first()
        form = AssistantHandlerForm(obj=assistant)
        form.model_id.choices = model_choices
        form.version_id.choices = version_choices
        if assistant.apikey:
            form.apikey.data = assistant.apikey.apikey
        if form.validate_on_submit() and request.method == 'POST' and form.submit.data:
            current_app.logger.info(f'entro a actualizar asistente')   
            try:
                assistant.name = form.name.data
                assistant.model_id = form.model_id.data
                assistant.version_id = form.version_id.data
                assistant.instructions = form.instructions.data
                assistant.description = form.description.data
                current_app.logger.info(f'assistant: {assistant}')
                db.session.commit()
                flash("Asistente actualizado correctamente.", 'success')
                return redirect(url_for('home_blueprint.assistants'))
            except Exception as e:
                db.session.rollback()
                error_message = f"Error al actualizar el asistente: {str(e)}"
                flash(error_message, 'danger')
                error_traceback = traceback.format_exc()
                current_app.logger.error(f"{error_message}\n{error_traceback}")
        return render_template('home/assistant_form.html', segment='assistants-list', form=form, assistant=assistant)
    else:
        form = AssistantHandlerForm()
        form.model_id.choices = model_choices
        form.version_id.choices = version_choices
        if form.validate_on_submit() and request.method == 'POST':
            try:
                modelo = AssistantsModels.query.filter_by(id=form.model_id.data).first()
                data = {
                    'name': form.name.data,
                    'model_id': modelo.oa_name,
                    'version_id': form.version_id.data,
                    'instructions': form.instructions.data,
                    'description': form.description.data
                }
                current_app.logger.info(f'data: {data}')
                assistant_id = AssistantController().create_assistant(data)
                current_app.logger.info(f'assistant_id: {assistant_id}')
                assistant = Assistants(
                    id_openai = assistant_id,
                    name = form.name.data,
                    user_id = current_user.id,
                    model_id = form.model_id.data,
                    version_id = form.version_id.data,
                    instructions = form.instructions.data,
                    description = form.description.data
                )
                current_app.logger.info(f'assistant: {assistant}')
                db.session.add(assistant)
                db.session.commit()
                flash("Asistente creado correctamente.", 'success')
                return redirect(url_for('home_blueprint.assistants'))
            except Exception as e:
                db.session.rollback()
                error_message = f"Error al crear el asistente: {str(e)}"
                flash(error_message, 'danger')
                error_traceback = traceback.format_exc()
                current_app.logger.error(f"{error_message}\n{error_traceback}")
        return render_template('home/assistant_form.html', segment='assistants-list', form=form)

@blueprint.route('/assistant_addFile', methods=['POST'])
@login_required
def assistant_addFile():
    try:
        assistant_id = request.form.get('assistant_id')
        file = request.files.get('file')
        if not assistant_id or not file:
            return jsonify({'status': 'error', 'message': 'No se han recibido los datos necesarios'}), 400
        
        assistant = Assistants.query.get(assistant_id)
        if not assistant:
            return jsonify({'status': 'error', 'message': 'No se ha encontrado el asistente'}), 404
        
        # validar si el asistente ya tiene un vector, en caso contrario crearlo
        vector_obj = AssistantsVector.query.filter_by(assistant_id=assistant_id).first()
        if not vector_obj:
            vector_obj = AssistantsVector(assistant_id=assistant_id)
            db.session.add(vector_obj)
            db.session.commit()

        path = f'home/controller/files/{current_user.id}/{assistant_id}'
        absolute_path = os.path.join('website', path)
        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path)
        file_path = os.path.join(absolute_path, file.filename)
        file.save(file_path)
        assistantsFile = AssistantsFiles(name=file.filename, path=path, assistant_id=assistant_id, vector_id=vector_obj.id ,type=os.path.splitext(file.filename)[1], size= os.path.getsize(file_path))
        current_app.logger.info(f'assistantFile: {assistantsFile}') 
    except Exception as e:
        current_app.logger.error(traceback.format_exc())
    try:
        db.session.add(assistantsFile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(traceback.format_exc())
        error_traceback = traceback.format_exc()
        current_app.logger.error(f"Error al guardar el archivo: {str(e)}\n{error_traceback}")
        return jsonify({'status': 'error', 'message': str(error_traceback)}), 400
    
    # Devuelve los datos del archivo recién subido
    return jsonify({
        'status': 'success',
        'message': f'Archivo {file.filename} cargado correctamente.',
        'file': {
            'id': assistantsFile.id,
            'name': assistantsFile.name,
            'type': assistantsFile.type,
            'size': assistantsFile.size,
            'upload': assistantsFile.upload,
            'vector': assistantsFile.vector_id,
            'created_at': assistantsFile.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    }), 200

@blueprint.route('/assistant_run', methods=['POST'])
@login_required
def assistant_run():
    assistant_id = request.form.get('assistant_id')
    if not assistant_id:
        return jsonify({'status': 'error', 'message': 'No se ha especificado el asistente'}), 400
    assistant = Assistants.query.get(assistant_id)
    if not assistant:
        return jsonify({'status': 'error', 'message': 'No se ha encontrado el asistente'}), 404
    # Obtener los archivos no subidos desde la base de datos
    files = AssistantsFiles.query.filter_by(assistant_id=assistant_id, upload=False).all()
    current_app.logger.info(f'files to upload: {files}')
    if not files:
        return jsonify({'status': 'error', 'message': 'No se han encontrado archivos para subir'}), 404

    file_paths = [os.path.join('website', file.path, file.name) for file in files]
    name = f'{assistant.name}-Datos'
    data = {
        'name': name,
        'file_path': file_paths,
        'assistant_id': assistant.id_openai
    }
    try:
        vector = AssistantsVector.query.filter_by(assistant_id=assistant_id).first()
        assistant_openai, vector_store_id = AssistantController().run_assistant(data, assistant.id, vector)
        current_app.logger.info(f'vector_store_id: {vector_store_id}')
        vector.vector = vector_store_id
        db.session.commit()
        assistant.vector_id = vector.id
        # Actualizar estado de los archivos
        updated_files = []
        for file in files:
            file_obj = AssistantsFiles.query.get(file.id)
            file_obj.upload = True
            updated_files.append({
                'id': file_obj.id,
                'upload': file_obj.upload
            })
        db.session.commit()
        flash("Asistente ejecutado correctamente.", 'success')
        # Prepara los datos para la respuesta
        current_app.logger.info(f'updated_files: {updated_files}')
        return jsonify({'status': 'success', 'updated_files': updated_files}), 202
    except Exception as e:
        error_message = f"Error al ejecutar el asistente: {str(e)}"
        flash(error_message, 'danger')
        error_traceback = traceback.format_exc()
        current_app.logger.error(f"{error_message}\n{error_traceback}") 
        return jsonify({'status': 'error', 'message': str(error_traceback)}), 400
    

@blueprint.route('/download_file/<file_id>', methods=['GET'])
@login_required
def download_file(file_id):
    file = AssistantsFiles.query.get(file_id)
    if not file:
        flash("No se ha encontrado el archivo", 'danger')
        return jsonify({'status': 'error', 'message': 'No se ha encontrado el archivo'}), 404
    file_path = os.path.join(file.path, file.name)
    return send_file(file_path, as_attachment=True)
    

@blueprint.route('/create-assistant', methods=['POST', 'GET'])
@login_required
def create_assistant():
    return render_template('home/create_assistant.html', segment='assistants')

@blueprint.route('/threads', methods=['GET'])
@login_required
def threads():
    return render_template('home/threads.html', segment='threads')

@blueprint.route('/api_key', methods=['GET'])
@login_required
def api_key():
    flash("Entro al menu de ApiKey",'info')
    return render_template('home/api_key.html', segment='api_key')

@blueprint.route('/generate_apikey', methods=['POST'])
@login_required
def generate_apikey():
    data = request.get_json()
    assistant_id = data.get('assistant_id')
    if not assistant_id:
        return jsonify({'status': 'error', 'message': 'No se ha especificado el asistente'}), 400
    try:
        api_key = secrets.token_urlsafe(16)
        apikeyObj = AssistantsApiKey(apikey=api_key, assistant_id=assistant_id)
        db.session.add(apikeyObj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        error_traceback = traceback.format_exc()
        current_app.logger.error(f"Error al generar la clave de API: {str(e)}\n{error_traceback}")
        return jsonify({'status': 'error', 'message': str(error_traceback)}), 400    
    return jsonify({'status': 'success', 'apikey': api_key}), 202

@blueprint.route('/ApiKeyAssistantCopy/<assistant_id>', methods=['GET'])
@login_required
def ApiKeyAssistantCopy(assistant_id):
    try:
        assistant = Assistants.query.get(assistant_id)
        if assistant and assistant.apikey:
            return jsonify({'apikey': assistant.apikey.apikey})
    except Exception as e:
        error = traceback.format_exc()
        current_app.logger.error(f"Error al copiar la clave de API: {str(e)}\n{error}")
        return jsonify({'status': 'error', 'message': str(error)}), 400
    
@blueprint.route('/chatbot/<assistant_id>', methods=['GET','POST'])
@login_required
def chatbot(assistant_id):
    form = AssistantForm()
    assistant = Assistants.query.get(assistant_id)
    return render_template('home/chatbot.html', segment='chatbot', form=form, assistant=assistant)

@blueprint.route('/finanzas', methods=['GET','POST'])
@login_required
def finance():
    form = AssistantForm()
    return render_template('home/finance.html', segment='finance', form=form)

@blueprint.route('/credit', methods=['GET','POST'])
@login_required
def credit():
    form = AssistantForm()
    return render_template('home/credit.html', segment='credit', form=form)

@blueprint.route('/api/get-thread', methods=['GET'])
@csrf.exempt
@require_api_key
def getThread():
    thread_id = session.get('thread_id')
    return jsonify({'status': 'success', 'thread_id': thread_id}), 200

@blueprint.route('/api/virtual-agent', methods=['POST'])
@csrf.exempt
@require_api_key
def virtualAgent():
    
    CORS_DATA = {'Access-Control-Allow-Origin':'*',
                                    'Access-Control-Allow-Methods':'PUT,DELETE',
                                    'Access-Control-Allow-Headers':'content-type'}
    
    # Obtener datos de los headers
    apikey = request.headers.get('API-KEY')
    user_id = request.headers.get('USER-ID')
    
    assistantApiKey = AssistantsApiKey.query.filter_by(apikey=apikey).first()
    assistantObj = Assistants.query.filter_by(id=assistantApiKey.assistant_id).first()
    
    # Comprobar si los headers existen
    if not apikey or not user_id:
        return jsonify({'status': 'error', 'message': 'Faltan datos en los headers'}), 400 , CORS_DATA
    
    request_data = request.get_json()
    if not request_data or not request_data.get('message'):
        return jsonify({'status': 'error', 'message': 'No se ha recibido información'}), 400, CORS_DATA
    
    message = request_data.get('message')
    print(f'Mensaje recibido: {message}')

    # Obtén el thread_id de la sesión si existe, o genera uno nuevo
    thread_id = request_data.get('thread_id')
    if not thread_id:
        # Aquí deberías crear un nuevo thread_id y guardarlo en la sesión
        assistant = AssistantController(client_id=user_id, thread_id=None)
        thread_id = assistant.thread_id
        session['thread_id'] = thread_id
    current_app.logger.info(f'thread type : {type(thread_id)}')
    current_app.logger.info(f"Thread ID: {thread_id}")
    
    # Inicializa el controlador del asistente con los datos obtenidos
    assistant = AssistantController(client_id=user_id, thread_id=thread_id)
    data = {
        'message': message,
        'thread_id': thread_id,
        'assistant_id': assistantObj.id_openai
    }
    response = assistant.sendMessage(data)
    
    # Procesa la respuesta para asegurar que es serializable
    # messages = [{
    #     'id': msg.id,
    #     'content': msg.content[0].text.value,
    #     'type': 'response'
    # } for msg in response.data]
    
    # Actualiza el thread_id en la sesión si ha cambiado
    session['thread_id'] = assistant.thread_id
    
    return jsonify({
        'status': 'success',
        'message': response.value,
        'asistente': assistantObj.name,
        'image_url': 'images/greetbotix.png',
        'time': datetime.now().strftime('%d %b %I:%M %p'),
        'type': 'chatbot',
        'thread_id': thread_id 
    }), 202 , CORS_DATA



@blueprint.route('/enviar_mensaje', methods=['POST'])
@login_required
def enviar_mensaje():
    current_app.logger.info("Enviando mensaje")
    form = AssistantForm()
    if form.validate_on_submit():
        data1 = request.get_json()
        assistantObj = Assistants.query.get(data1.get("assistant_id"))
        current_app.logger.info(f'{data1}') 
        # Obtener el thread_id de la sesión
        thread_id = session.get('thread_id')
        current_app.logger.info(f"Thread ID: {thread_id}")
        assistant = AssistantController(client_id=current_user.id, thread_id=thread_id)
        data = {
        'message': data1.get("message"),
        'thread_id': assistant.thread_id,
        'assistant_id': assistantObj.id_openai
    }
        response = assistant.sendMessage(data)
        current_app.logger.info(f"Respuesta recibida: {response}")

        # # Procesar la respuesta para asegurar que es serializable
        # messages = [{
        #     'id': msg.id,
        #     'content': msg.content[0].text.value,  # Asumiendo estructura de la respuesta
        #     'type': 'response'
        # } for msg in response.data]  # Ajusta esto según la estructura real de 'response'
        

        # Actualizar el thread_id en la sesión si ha cambiado
        session['thread_id'] = assistant.thread_id
    
        return jsonify({
            'status': 'success',
            'message': response.value,
            'username': assistantObj.name,
            'image_url': assistantObj.avatar_path,
            'time': datetime.now().strftime('%d %b %I:%M %p'),
            'type': 'chatbot'
        }), 202 

    else:
        # Registrar los errores si la validación falla
        current_app.logger.error(f"Errores del formulario: {form.errors}")
        return jsonify({'status': 'error', 'errors': form.errors}), 400


@blueprint.route('/ecommerce', methods=['POST','GET'])
@login_required
def ecommerce():
    form = CounterAssistantForm()
    return render_template('home/ecommerce.html', form=form, segment='ecommerce')