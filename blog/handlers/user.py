import re

from google.appengine.ext import db

import base
from entities import user_entity as user


##### Global Functions

USER_RE = re.compile(r'^[\w-]{3,20}$')
def valid_username(username):
   """
   check if username is a valid format
   """
   return username and USER_RE.match(username)


PASSWD_RE = re.compile(r'^.{3,20}$')
def valid_password(password):
   """
   check if password is a valid format
   """
   return password and PASSWD_RE.match(password)


EMAIL_RE = re.compile(r'^\S+@\S+\.\S+$')
def valid_email(email):
   """
   check if email is a valid format
   """
   return email and EMAIL_RE.match(email)


##### User Signup/Login/Logout handlers

class SignupPageHandler(base.BaseHandler):
   """
   handles '/signup'
   display the signup page and set cookie for user
   redirect to welcome page
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
         u = user.User.by_name(username)

         if u:
            self.render('signup-form.html',
                        error_username='Username already exists')
         else:
            u = user.User.create(username, password, email)
            u.put()        # store user in database
            self.login(u)  # set cookie for current user
            self.redirect('/welcome')



class LoginPageHandler(base.BaseHandler):
   """
   handles '/login'
   display the login page and set cookie for user
   redirect to welcome page
   """
   def get(self):
      self.render('login-form.html')


   def post(self):
      username = self.request.get('username')
      password = self.request.get('password')

      if username and password:

         u = user.User.login(username, password)

         if u:
            self.login(u)  # set cookie for current user
            self.redirect('/welcome')

         else:
            self.render('login-form.html',
               error_msg='Invalid username or password')



class LogoutHandler(base.BaseHandler):
   """
   handles '/logout'
   delete cookie for current user
   redirect to signup page
   """
   def get(self):
      self.logout()
      self.redirect('/login')






