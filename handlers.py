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
import tornado.web

# Bibtex parsing
from pybtex.database.input import bibtex
from operator import itemgetter, attrgetter


###############################################################################
# Custom Error Handler
###############################################################################
class CustomErrorHandler(tornado.web.RequestHandler):
    """Generates an error response with status_code for all requests."""
    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)

    def write_error(self, status_code, **kwargs):
        error_trace = None
        if self.settings.get("debug") and "exc_info" in kwargs:
            import traceback
            error_trace= ""
            for line in traceback.format_exception(*kwargs["exc_info"]):
                error_trace += line
        self.render("error.html", status_code=status_code, error_trace=error_trace)

# Use this new Error Handler
tornado.web.ErrorHandler = CustomErrorHandler

###############################################################################
# Base handler. All the handlers should inherit from it.
###############################################################################
class BaseHandler(tornado.web.RequestHandler):
    # Override error write handler
    def write_error(self, status_code, **kwargs):
        err = tornado.web.ErrorHandler(self.application, self.request, status_code=status_code)
        err._transforms = []
        self._finished = True
        self.set_status(status_code)
        err.write_error(status_code, **kwargs)


    def _nolog(self):
        print "NOLOG"

class HomeHandler(BaseHandler):
    def get(self):
        self.redirect("/home")
#
class PageHandler(BaseHandler):
    def get(self, page):
        # Check if the file exists
        # otherwise throw a 404 error
        if page == "error":
            raise tornado.web.HTTPError(404, "Not found")
        try:
            self.render(page + ".html")
        except IOError, e: 
            raise tornado.web.HTTPError(404, "Not found")

class PapersHandler(BaseHandler):
    def get(self):
        papers = []
        parser = bibtex.Parser()
        try:
            bib_data = parser.parse_file('./static/papers/papers.bib')
        except IOError, e:
            raise tornado.web.HTTPError(404, "Not Found")

        sorted_keys = sorted(bib_data.entries, key=lambda k: bib_data.entries[k].fields['year'], reverse=True)
        entries = bib_data.entries
        for k in sorted_keys:
            paper = {}
            paper['name'] = k
            paper['title'] = entries[k].fields['title']
            paper['year'] = entries[k].fields['year']
            paper['where'] = entries[k].fields['journal']

            if entries[k].fields.has_key('howpublished'):
                paper['slides-url'] = entries[k].fields['howpublished']

            # Get paper authors
            authors = []
            persons = entries[k].persons['author']
            for p in persons:
                authors.append(p.first()[0] + " " + p.last()[0])
            paper['authors'] = ", ".join(authors)
            # Do we have a file for the abstract ? 
            absfile = './static/papers/' + k + '_abstract.txt'
            if os.path.exists(absfile) and os.path.isfile(absfile):
                paper['abstract'] = " ".join(open(absfile, 'r').readlines())
            # Do we have a file for the article document ?
            docfile = './static/papers/' + k + '.pdf'
            if os.path.exists(docfile) and os.path.isfile(docfile):
                paper['document'] = self.static_url('papers/' + k + '.pdf')
            sldfile = './static/papers/' + k + '_slides.pdf'
            # Do we have a file for the article slides ?
            if os.path.exists(sldfile) and os.path.isfile(sldfile):
                paper['slides'] = self.static_url('papers/' + k + '_slides.pdf')


            papers.append(paper)
        self.render("papers.html", papers=papers)


