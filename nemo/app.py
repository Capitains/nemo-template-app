from flask import Flask
from capitains_nautilus.flask_ext import FlaskNautilus


from . import configurable


app = Flask("app")


extension_nemo = configurable.nemo_class(
    base_url="",
    resolver=configurable.resolver,
    templates={"main": configurable.templates_folder},
    chunker={
        "default": configurable.chunker
    }
)
extension_nautilus = FlaskNautilus(
    prefix="/api",
    resolver=configurable.resolver
)


extension_nautilus.init_app(app)
extension_nemo.init_app(app)
