from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField, FileField
from wtforms.validators import DataRequired

class AssistantForm (FlaskForm):
    message = StringField('Mensaje', id='mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar', render_kw={'id': 'submit-button'})
    
    
class CounterAssistantForm (FlaskForm):
    message = StringField('Mensaje', id='mensaje', validators=[DataRequired()], render_kw={'placeholder':'Escribe tu mensaje'})
    
class AssistantHandlerForm(FlaskForm):
    id = HiddenField('ID', id='id', render_kw={'readonly': True})
    id_openai = HiddenField('ID OpenAI', id='id_openai', render_kw={'readonly': True})
    name = StringField('Nombre del asistente', id='name', validators=[DataRequired()])
    model_id = SelectField('Modelo', id='model_id', coerce=str, validators=[DataRequired()])
    version_id = SelectField('Versión', id='version_id', coerce=str, validators=[DataRequired()])
    description = StringField('Descripción', id='description', validators=[DataRequired()])
    instructions = StringField('Instrucciones', id='instructions', validators=[DataRequired()])
    apikey = StringField('API Key', id='apikey', render_kw={'readonly': True})
    avatar = FileField('Avatar', id='avatar')
    submit = SubmitField('Guardar', render_kw={'id': 'submit-button'})

class AssistantFileForm(FlaskForm):
    file = FileField('Selecciona el archivo', id='customFile', validators=[DataRequired()])
    save = SubmitField('Enviar', render_kw={'id': 'submit-button'})
    cancel = SubmitField('Cancelar', render_kw={'id': 'cancel-button'})

class ModelsForm(FlaskForm):
    id = StringField('ID', id='id', render_kw={'readonly': True})
    name = StringField('Nombre del modelo', id='name', validators=[DataRequired()])
    active = StringField('Activo', id='active', validators=[DataRequired()])
    