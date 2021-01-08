from flask import render_template, url_for, flash, redirect, request, Blueprint

nas = Blueprint('nas', __name__)

@nas.route('/', methods=['GET', 'POST'])
def mainTeamIndex():
    return render_template('index.html')
