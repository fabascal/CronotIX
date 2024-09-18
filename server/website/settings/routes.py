from website.settings import blueprint
from flask import render_template, flash, current_app
from flask_login import login_required, current_user
from website.home.models import AssistantsModels, AssistantsVersion
from website.auth.models import User



########################
# Apartado de usuarios #
########################
@blueprint.route('/configuracion_usuario', methods=['GET'])
def user_settings():
    user = User.query.get(current_user.id)
    if not user:
        return flash('No se ha encontrado el usuario', 'danger')
    current_app.logger.info(f'User settings for user_id: {user}')
    return render_template('settings/user_settings.html')




@blueprint.route('/listar_modelos', methods=['GET'])
@login_required
def list_models():
    models = AssistantsModels.query.all()
    return render_template('settings/models_list.html', segment='assistants-models', models=models)

@blueprint.route('/listar_versiones', methods=['GET'])
@login_required
def list_versions():
    versions = AssistantsVersion.query.all()
    return render_template('settings/versions_list.html', segment='assistants-version', versions=versions)

@blueprint.route('/modelos/form', methods=['GET', 'POST'])
@blueprint.route('/modelos/form/<model_id>', methods=['GET', 'POST'])
@login_required
def handle_model_form(model_id=None):
    current_app.logger.info(f'Handling model form for model_id: {model_id}')
    return render_template('settings/models_form.html', segment='assistants-models')


@blueprint.route('/versiones/form', methods=['GET', 'POST'])
@blueprint.route('/versiones/form/<version_id>', methods=['GET', 'POST'])
@login_required
def handle_version_form(version_id=None):
    current_app.logger.info(f'Handling version form for version_id: {version_id}')
    return render_template('settings/versions_form.html', segment='assistants-version')