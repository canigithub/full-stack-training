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