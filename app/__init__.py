from flask import Flask
from flask_restx import Api
from app.core.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    api = Api(
        app,
        version="1.0",
        title="PDF Tables Extractor API",
        description="PDF Processing Service",
    )

    from app.api.pdf_namespace import ns as pdf_ns

    api.add_namespace(pdf_ns, path="/pdf")

    return app
