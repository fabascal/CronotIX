from website.settings import blueprint
from flask import render_template


@blueprint.route('/settings', methods=['GET'])  
def get_settings():
    print('Settings')
    return render_template('settings/settings.html')