from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_manager
import os

primary = Blueprint('primary', __name__)

@primary.route('/', methods=['GET', 'POST'])
def index(): 
    if current_user.is_authenticated:
        folder_path = r'C:/Users/Chris/Documents/Code/rasPi/nas/files'
        fileNames = os.listdir(folder_path)
        return render_template('index.html', fileNames=fileNames)
    else: return redirect(url_for('users.login'))