#!/usr/bin/env python
# coding utf-8
import argparse
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from server import my_app

APPNAME = "KPKI"

if __name__ == "__main__":
    opt = argparse.ArgumentParser(description="Server to web interface of %s" % APPNAME)
    opt.add_argument("--host", default="")
    opt.add_argument("--port", default=5000)
    opt.add_argument("--debug", "-d", default=False, action="store_true")
    args = opt.parse_args()

    http_server = WSGIServer((args.host, args.port), my_app,
            handler_class=WebSocketHandler)
    http_server.serve_forever()
