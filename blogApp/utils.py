import secrets
import os
import base64
import bleach
from flask import current_app


def save_file(file, path):
    """Save base64 encoded file in given path

    Parameters
    ----------
    file : str base64 encoded file
    path : path in which file is to be saved
    """
    file = file.partition(",")[2]  # get encoded info of file

    # generate a random name for file
    random_hex = secrets.token_hex(6)
    updated_file_name = random_hex+'.jpeg'
    # create a full path for saving file
    file_path = os.path.join(current_app.root_path, path, updated_file_name)

    with open(file_path, 'wb') as fh:
        # decode base64 string after converting to bytes
        fh.write(base64.decodebytes(bytes(file, 'utf-8')))

    return updated_file_name


def bleach_tags(content):
    """Remove unwanted HTML tags from str content

    Parameters
    ----------
    content : str
    """
    allowed_tags = ['span', 'p', 'img', 'a', 'br', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'u',
                    'blockquote', 'font', 'iframe', 'pre', 'ol', 'li', 'ul', 'div', 'table', 'tbody', 'td', 'tr']
    allowed_attrs = {
        '*': ['style', 'color', 'class'],
        'div': ['bis_skin_checked'],
        'a': ['href', 'target'],
        'img': ['src', 'class'],
        'iframe': ['frameborder', 'src', 'width', 'height']
    }
    allowed_styles = ['background-color', 'text-align',
                      'margin-left', 'width', 'float']
    # allow only tags in allowed_tags list, attributes in allowed_attrs, styles in allowed_styles
    clean_content = bleach.clean(
        content, tags=allowed_tags, attributes=allowed_attrs, styles=allowed_styles)
        
    return(clean_content)
