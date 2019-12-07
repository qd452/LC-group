from flask import Flask
from flask_restplus import Api
from werkzeug.contrib.fixers import ProxyFix
from .user import user_ns
from .contest import contest_ns
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app,
    version='1.0',
    title='LC Contest API',
    description='A simple LC contest API',
)

api.add_namespace(user_ns)
api.add_namespace(contest_ns)

