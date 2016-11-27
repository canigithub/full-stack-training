import base

class MainPageHandler(base.BaseHandler):
   """
   handles '/'
   display main page.
   """
   def get(self):
      self.render("mainpage.html")