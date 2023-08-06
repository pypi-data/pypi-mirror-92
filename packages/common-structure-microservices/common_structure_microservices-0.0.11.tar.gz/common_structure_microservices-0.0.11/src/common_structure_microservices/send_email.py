import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from src.common_structure_microservices import exception


def send_email(file, send_to_list, subject, images=None, context=None):
    kwargs = {
        'subject': subject,
        'body': None
    }
    kwargs.update({'to': send_to_list})
    email = EmailMessage(**kwargs)
    if images is None:
        images = []

    html_content = render_to_string(file, context=context)
    html_attachment = _attach_content_email(images, html_content)
    email.attach(html_attachment)
    email.attach_file(images[0])

    try:
        email.send()
    except smtplib.SMTPException:
        raise exception.SendEmailError


def _attach_content_email(subject, files=None, html_content=None):
    html_part = MIMEMultipart(_subtype='related')
    html_part.attach(MIMEText(html_content, _subtype='html'))
    html_part['Subject'] = subject

    if files is None:
        files = []

    for file in files:
        _file = MIMEImage(file['data'], file['extension'])
        _file.add_header('Content-Id', f"<{file['name']}>")
        _file.add_header("Content-Disposition", "inline", filename=file['name'])
        html_part.attach(_file)

    return html_part


def _get_data_image(file, base_dir, path, data=None):
    if data is None:
        path_template = f"{Path(path)}{os.sep}"
        path_image = base_dir + path_template + file[0] + '.' + file[1]
        data = open(path_image, 'rb').read()

    return {
        'name': file[0],
        'extension': file[1],
        'data': data
    }
