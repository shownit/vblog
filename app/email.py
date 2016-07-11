#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app, render_template
from flask_mail import Message

from .tasks import send_async_email


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    subject = app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject
    sender = app.config['MAIL_SENDER']
    msg = Message(subject, sender=sender, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    send_async_email.delay(msg)
