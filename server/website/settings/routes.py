from website.settings import blueprint
from flask import render_template
from flask_login import login_required


@blueprint.route('/settings', methods=['GET'])  
def get_settings():
    print('Settings')
    return render_template('settings/settings.html')


@blueprint.route('/account_settings', methods=['GET', 'POST'])
@login_required
def account_settings():
    return render_template('settings/account_settings.html')
