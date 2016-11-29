import base

class MainPageHandler(base.BaseHandler):
   """
   handles '/'
   display main page.
   """
   def get(self):
      if not self.user:
         self.render("/logged-out/mainpage-out.html")
      else:
         self.render("/logged-in/mainpage-in.html", username=self.user.name)