from flask import Flask
from .database import AppDatabase, pw
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.cfg')
    
    fmt = "%(levelname)s - %(asctime)s %(filename)s:%(lineno)d %(message)s"
    formatter = logging.Formatter(fmt=fmt)
    log_path = './{}.log'.format(__name__)
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    return app

app = create_app()

from yankes_api.command import db_migrate, sync_data

app.cli.add_command(db_migrate)
app.cli.add_command(sync_data)

import yankes_api.routes
