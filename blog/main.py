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

import os
import re

import webapp2
import jinja2

from google.appengine.ext import db

ERROR_MSG = "Please fill both subject and content!"

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                autoescape=True)


###### Base handler class

def render_str(template, **param):
   """
   Given template and parameters, return the rendered text
   """
   t = jinja_env.get_template(template)
   return t.render(param)

class BaseHandler(webapp2.RequestHandler):
   """
   The base handler that will be extended by other handlers
   """
   def write(self, text):
      """
      Write the response back to browser
      """
      self.response.write(text);

   def render(self, template, **param):
      """
      Render the view back to browser given template and parameters
      """
      self.write(render_str(template, **param))

class MainPageHandler(BaseHandler):
   """
   handle '/'
   """
   def get(self):
      self.write('Hello Visiter!')


###### Blog

def blog_key(name='default'):
   """
   default parent key: 'blogs/default'
   """
   return db.Key.from_path('blogs', name)

class Post(db.Model):
   """
   Post object:
      subject - title of the post
      content - content of the post
      created_time - post created time
      last_modified - time of the most recent modify
   """
   subject = db.StringProperty(required=True)
   content = db.TextProperty(required=True)
   create_time = db.DateTimeProperty(auto_now_add=True)
   last_modified = db.DateTimeProperty(auto_now=True)

   def render(self):
      """
      return the html-version text of the post
      """
      self.render_content = self.content.replace('/n', '<br>')
      return render_str('post.html', p=self)


class BlogFrontHandler(BaseHandler):
   """
   handles '/blog' and display 10 most recent posts
   """
   def get(self):
      posts = db.GqlQuery("select * from Post order by create_time desc limit 10")
      self.render("front.html", posts=posts)


class NewPostHandler(BaseHandler):
   """
   handles '/blog/newpost'. let user submit new posts using POST method
   """
   def get(self):
      self.render("newpost.html")

   def post(self):
      subject = self.request.get("subject")
      content = self.request.get("content")

      if subject and content:
         p = Post(parent=blog_key(), subject=subject, content=content)
         p.put()
         self.redirect("/blog/%s" % str(p.key().id()))
      else:
         self.render("newpost.html", subject=subject, content=content, error_msg=ERROR_MSG)


class NewPostPageHandler(BaseHandler):
   """
   handle '/blog/(\d+)', display the newly created post
   """
   def get(self, post_id):
      key = db.Key.from_path('Post', int(post_id), parent=blog_key())
      post = db.get(key)

      if not post:
         self.error(404)
         return

      self.render("permalink.html", p=post)


###### Signup

USER_RE = re.compile(r'^[\w-]{3,20}$')
def valid_username(username):
   return username and USER_RE.match(username)

PASSWD_RE = re.compile(r'^.{3,20}$')
def valid_password(password):
   return password and PASSWD_RE.match(password)

EMAIL_RE = re.compile(r'^\S+@\S+\.\S+$')
def valid_email(email):
   return email and EMAIL_RE.match(email)


class SignupPageHandler(BaseHandler):
   """
   handle '/blog/signup'
   """
   def get(self):
      self.render('signup-form.html')

   def post(self):
      is_error = False
      username = self.request.get('username')
      password = self.request.get('password')
      verify = self.request.get('verify')
      email = self.request.get('email')

      params = dict(username=username, email=email)

      if not valid_username(username):
         params['error_username'] = 'Not valid username'
         is_error = True

      if not valid_password(password):
         params['error_password'] = 'Not valid password'
         is_error = True
      elif password != verify:
         params['error_verify'] = 'Password not match'
         is_error = True

      if email and not valid_email(email):
         params['error_email'] = 'Not valid email'
         is_error = True

      if is_error:
         self.render('signup-form.html', **params)
      else:
         self.redirect('/blog/welcome')


class WelcomePageHandler(BaseHandler):
   """
   handle '/blog/welcome'
   """
   def get(self):
      self.write('Welcome!')

###### Register routing

app = webapp2.WSGIApplication([
      ('/', MainPageHandler),
      ('/blog', BlogFrontHandler),
      ('/blog/newpost', NewPostHandler),
      ('/blog/(\d+)', NewPostPageHandler),
      ('/blog/signup', SignupPageHandler),
      ('/blog/welcome', WelcomePageHandler)
], debug=True)
