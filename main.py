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
import logging

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
	title= db.StringProperty(required=True)
	art = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add = True)

class MainHandler(Handler):
	#def render_front(self, title="", art="", error=""):
	#	self.render('ascii.html', title=title, art= art, error=error)

    def get(self):
        self.render("ascii.html")

    def post(self):
    	logging.getLogger().setLevel(logging.DEBUG)
    	title = self.request.get('title')
    	art = self.request.get('art')
    	
    	if title and art:
    		a = Art(title=title, art=art)
    		a.put()
    		#logging.info(art)
    		arts = db.GqlQuery("Select * from Art order by created desc")
    		for art in arts:
    			logging.info(art.title)
    			logging.info(art.art)
    		self.render('ascii.html', arts = arts)

    	else:
    		error = 'please input title and art'
    		self.render('ascii.html', title = title, art=art, error=error)


app = webapp2.WSGIApplication([ ('/', MainHandler)
], debug=True)
