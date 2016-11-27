import base

from google.appengine.ext import db
from entities import blog as Blog


##### Blog Handlers

class BlogFrontPageHandler(base.BaseHandler):
   """
   handles '/blog'
   display the main page of blog section.
   """
   def get(self):
      posts = db.GqlQuery('select * from Post order by created desc limit 10')
      self.render('blog-front.html', posts=posts)


class AddNewPostPageHandler(base.BaseHandler):
   """
   handles '/blog/newpost'
   display the page to create new post.
   redirect to permalink page
   """
   def get(self):
      """
      if is (signed in) user, render new post page;
      otherwise, redirect to login page
      """
      if self.user:
         self.render('newpost.html')
      else:
         self.redirect('/login')


   def post(self):
      """
      if not user, redirect to blog front page
      """
      if not self.user:
         self.redirect('/blog')

      subject = self.request.get('subject')
      content = self.request.get('content')

      if subject and content:
         p = Blog.Post(parent=Blog.blog_key(), subject=subject, content=content)
         p.put()
         self.redirect('/blog/%s' % str(p.key().id()))
      else:
         self.render('newpost.html',
                     subject=subject,
                     content=content,
                     error_msg='Enter both subject and content, please!')



class PermalinkPageHandler(base.BaseHandler):
   """
   handles '/blog/(\d+)' where the number is the post id
   display the newly created post.
   """
   def get(self, post_id):
      key = db.Key.from_path('Post', int(post_id), parent=Blog.blog_key())
      post = db.get(key)

      if not post:
         self.error(404)
      else:
         self.render('permalink.html', p=post)













