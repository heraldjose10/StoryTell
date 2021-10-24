import secrets
import os
import base64
import bleach
from flask import current_app


def save_file(file, path):
    file = file.partition(",")[2]
    random_hex = secrets.token_hex(8)
    updated_file_name = random_hex+'.jpeg'
    file_path = os.path.join(current_app.root_path, path, updated_file_name)

    with open(file_path, 'wb') as fh:
        fh.write(base64.decodebytes(bytes(file, 'utf-8')))

    return updated_file_name


def bleach_tags(to_bleach):
    allowed_tags = ['span', 'p', 'img', 'a', 'br', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'u',
                        'blockquote', 'font', 'iframe', 'pre', 'ol', 'li', 'ul', 'div', 'table', 'tbody', 'td', 'tr']
    attrs = {
        '*': ['style', 'color', 'class'],
        'div': ['bis_skin_checked'],
        'a': ['href', 'target'],
        'img': ['src', 'class'],
        'iframe': ['frameborder', 'src', 'width', 'height']
    }
    styles = ['background-color', 'text-align',
                'margin-left', 'width', 'float']
    clean_content = bleach.clean(
        to_bleach, tags=allowed_tags, attributes=attrs, styles=styles)
    return(clean_content)