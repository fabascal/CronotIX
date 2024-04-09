from flask import render_template, current_app, flash
from flask_login import login_required
from website.home import blueprint

@blueprint.route('/', methods=['GET'])
def index():
    return render_template('home/index.html')

@blueprint.route('/assistants', methods=['GET'])
@login_required
def assistants():
    return render_template('home/assistants.html', segment='assistants')

@blueprint.route('/tunning', methods=['GET'])
@login_required
def tunning():
    return render_template('home/tunning.html', segment='tunning')

@blueprint.route('/api_key', methods=['GET'])
@login_required
def api_key():
    flash("Usuario creado correctamente.",'success')
    return render_template('home/api_key.html', segment='api_key')