from flask import Blueprint, redirect, render_template, request, send_from_directory

conduct_views = Blueprint('conduct_views', __name__, template_folder='../templates')

@conduct_views.route('/conduct', methods=['GET'])
def conduct_page():
    return render_template('conduct.html')

