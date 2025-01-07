from flask import Flask
from flask_bootstrap import Bootstrap

#pas5: Dins init.py, li hem de pasar la configuració de la app i importar la clase config
from .config import Config

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    
    #pas5: Dins app.py, li hem de pasar la configuració de la app i importar la clase config
    app.config.from_object(Config)
    return app
