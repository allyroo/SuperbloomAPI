from flask import Blueprint, render_template

"""
    Some arguments are specified when creating the Blueprint object.
    The first argument "site", is the blueprint name, 
    which is used by Flask's routing mechanism

    The second argument, __name__, is the Blueprint's import name
    this is how flask locates the blueprint's resources
"""

site = Blueprint('site',__name__,template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')