#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from . import create_celery_app, mail

celery = create_celery_app()


@celery.task
def send_async_email(msg):
    app = current_app._get_current_object()
    with app.app_context():
        mail.send(msg)
