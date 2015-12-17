#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader("%s/templates/" % os.path.dirname(__file__)))
    #loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

from models import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}

        template = jinja_environment.get_template('index.html')
        self.response.write(template.render(template_values))

class PubHandler(webapp2.RequestHandler):
    def get(self):
        import yaml
        pubs = yaml.load(open("%s/pubs.yaml" % os.path.dirname(__file__)).read())

        for pub in pubs['articles']:
            links = []
            pub['links'] = []
            if pub.has_key('website'):
                if pub['website'].startswith('http'):
                    links.append((pub['website'], pub['website'][7:].rstrip('/')))
            if pub.has_key('doi'): links.append(('http://dx.doi.org/%s' % pub['doi'], 'DOI'))
            if pub.has_key('pdf'): links.append(('/static/pubs/%s' % pub['pdf'].replace(' ', '_'), 'PDF'))
            if pub.has_key('git'): links.append((pub['git'], 'GitHub'))

            for url,title in links:
                pub['links'].append("<a href='%s'>%s</a>" % (url, title))

        for pub in pubs['bookchapter']:
            links = []
            pub['links'] = []
            if pub.has_key('website'):
                if pub['website'].startswith('http'):
                    links.append((pub['website'], pub['website'][7:].rstrip('/')))
            if pub.has_key('doi'): links.append(('http://dx.doi.org/%s' % pub['doi'], 'DOI'))
            if pub.has_key('pdf'): links.append(('/static/pubs/%s' % pub['pdf'].replace(' ', '_'), 'PDF'))

            for url,title in links:
                pub['links'].append("<a href='%s'>%s</a>" % (url, title))

        template_values = {"pubs": pubs}
        template = jinja_environment.get_template('pubs.html')
        self.response.write(template.render(template_values))

class ContactHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {}

        template = jinja_environment.get_template('contact.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/pubs/', PubHandler),
    ('/contact/', ContactHandler)
], debug=True)
