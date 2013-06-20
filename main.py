#!/usr/bin/env python
#
# Copyright 2011 Luca Niccolini - luca.niccolini@gmail.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import sys

import tornado.web
import tornado.wsgi
import wsgiref.handlers


import handlers

settings = {
    "title": u"Luca Niccolini",
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "xsrf_cookies": True,
    "autoescape": None,
    "debug": True
}


handlers_config = [
    (r"/", handlers.HomeHandler),
    (r"/papers", handlers.PapersHandler),
    (r"/([a-z]*)", handlers.PageHandler)
];

def main_gae():
    import webapp2
    # Deprecated: webapp version 1
    #from google.appengine.ext import webapp
    #from google.appengine.ext.webapp import util
    #from google.appengine.api import users
    #from google.appengine.ext import db

    application = tornado.wsgi.WSGIApplication(handlers_config, **settings)

    wsgiref.handlers.CGIHandler().run(application)


def main_tornado():
    import tornado.options
    import tornado.httpserver
    import tornado.ioloop
    from tornado.options import define, options

    # Define options
    define("port", default=80, help="Port on which to listen to incoming connections", type=int)

    application = tornado.web.Application(handlers_config, **settings)

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    if 'tornado' in sys.argv:
        main_tornado()
    else: 
        main_gae()

