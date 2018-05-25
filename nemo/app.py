from flask import Flask
from capitains_nautilus.flask_ext import FlaskNautilus


from . import configurable


app = Flask("app")


extension_nemo = configurable.nemo_class(
    base_url="",
    resolver=configurable.resolver,
    templates={
        "main": configurable.templates_folder,
        "additional": configurable.templates_folder_additional
    },
    chunker={
        "default": configurable.chunker
    },
    transform=configurable.xslt_dict,
    static_folder=configurable.statics_folder
)
extension_nautilus = FlaskNautilus(
    prefix="/api",
    resolver=configurable.resolver
)


extension_nautilus.init_app(app)
extension_nemo.init_app(app)

configurable.instantiate_errors(app, extension_nemo)
