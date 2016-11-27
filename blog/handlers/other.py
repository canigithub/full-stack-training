import base

class WelcomePageHandler(base.BaseHandler):
   """
   handles '/welcome'
   display welcome page after user login.
   """
   def get(self):
      if self.user:
         self.render('welcome.html', username=self.user.name)
      else:
         self.redirect('/signup')


class InvalidPageHandler(base.BaseHandler):
   """
   handles '/invalid/(\d+)'
   display welcome page after user login.
   """
   def get(self, code):
      if self.user:
         self.render('invalid.html', username=self.user.name, code=code)
      else:
         self.redirect('/blog')