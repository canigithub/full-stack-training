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
import os

import webapp2
import jinja2
import re

from google.appengine.ext import db

ERROR_MSG = "Please fill both subject and content!"

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape=True)


class Blog(db.Model):
   subject = db.StringProperty(required=True)
   content = db.TextProperty(required=True)
   create_time = db.DateTimeProperty(auto_now_add=True)


class BaseHandler(webapp2.RequestHandler):
   def write(self, text):
      self.response.write(text);

   def render_str(self, template, **param):
      t = jinja_env.get_template(template)
      return t.render(param)

   def render(self, template, **param):
      self.write(self.render_str(template, **param))


class BlogHandler(BaseHandler):
   def get(self):
      blogs = db.GqlQuery("select * from Blog order by create_time DESC")
      self.render("front.html", blogs=blogs)


class NewPostHandler(BaseHandler):
   def get(self):
      self.render("newpost.html")

   def post(self):
      subject = self.request.get("subject")
      content = self.request.get("content")
      if subject and content:
         new_blog = Blog(subject=subject, content=content)
         new_blog.put()
         blog_id = new_blog.key().id()
         self.redirect("/blog/" + str(blog_id))
      else:
         self.render("newpost.html", subject=subject, content=content, error_msg=ERROR_MSG)


class SingleBlogHandler(BaseHandler):
   def get(self, blog_id):
      newpost = Blog.get_by_id(int(blog_id))
      self.render("newblog.html", newpost=newpost)


app = webapp2.WSGIApplication([
    ('/blog', BlogHandler),
    ('/blog/newpost', NewPostHandler),
    ('/blog/(\d+)', SingleBlogHandler)
], debug=True)
