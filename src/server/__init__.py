#!/usr/bin/python
# coding: utf-8
import os

from flask import Flask
from websocket import handle_websocket

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.debug = True

def my_app(environ, start_response):  
    """This is basically an implementation as recommended at
    http://socketubs.net/2012/10/28/Websocket_with_flask_and_gevent/
    """
    path = environ["PATH_INFO"]  
    if path == "/":  
        return app(environ, start_response)  
    elif path == "/websocket":  
        handle_websocket(environ["wsgi.websocket"])   
    else:  
        return app(environ, start_response)  

import views

