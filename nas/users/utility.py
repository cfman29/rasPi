import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

def save_image(form_image):
    randome_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_filename = randome_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'static/profile_img', image_filename)
    final_size = (150, 150)
    i = Image.open(form_image)
    i.thumbnail(final_size)
    i.save(image_path)
    return image_filename

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset - HelloWorld!', sender='noreply@HelloWorld.com', recipients=[user.email])
    msg.body = f'''To reset your password click the link below.
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then ignore this email address.
    '''
    mail.send(msg)