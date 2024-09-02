from website.settings import blueprint
from flask import render_template
from flask_login import login_required
from website.home.models import AssistantsModels, AssistantsVersion


@blueprint.route('/settings', methods=['GET'])  
def get_settings():
    print('Settings')
    return render_template('settings/settings.html')


@blueprint.route('/account_settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    return render_template('settings/account_settings.html')


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
@blueprint.route('/modelos/form/<assistant_id>', methods=['GET', 'POST'])
@login_required
def handle_model_form(assistant_id=None):
    return render_template('settings/models_form.html', segment='assistants')
