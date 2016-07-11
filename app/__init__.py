#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_pagedown import PageDown
from config import config

db = SQLAlchemy()
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def register_blueprint(app):
    from .main import main
    from .auth import auth

    app.register_blueprint(main, url_prefix='')
    app.register_blueprint(auth, url_prefix='/auth')


def create_app(config_name, register_bp=True):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)

    if register_bp:
        register_blueprint(app)

    return app


def create_celery_app(app=None):
    config_name = os.getenv('VBLOG_CONFIG') or 'default'
    app = app or create_app(config_name, register_bp=False)
    celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
