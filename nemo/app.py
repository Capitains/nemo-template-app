from flask import Flask
from capitains_nautilus.flask_ext import FlaskNautilus


from .nemo import NemoTemplate
from . import nautilus


app = Flask("app")
extension_nemo = NemoTemplate(
    base_url="",
    resolver=nautilus.resolver
)
extension_nautilus = FlaskNautilus(
    prefix="/api",
    resolver=nautilus.resolver
)


extension_nautilus.init_app(app)
extension_nemo.init_app(app)
