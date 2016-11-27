from google.appengine.ext import db

import base
from entities import blog_entity as blog
from entities import like_entity as like

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
         p = blog.Post(parent=blog.blog_key(),
                  subject=subject,
                  content=content,
                  user_id=str(self.user.key().id()),
                  username=self.user.name)
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
      key = db.Key.from_path('Post', int(post_id), parent=blog.blog_key())
      post = db.get(key)

      if not post:
         self.error(404)
      else:
         self.render('permalink.html', p=post)



class EditPostPageHandler(base.BaseHandler):
   """
   handles '/blog/edit/(\d+)' where the number is the post id
   display the to be edited post
   """
   def get(self, post_id):
      if not self.user:
         self.redirect('/login')

      key = db.Key.from_path('Post', int(post_id), parent=blog.blog_key())
      post = db.get(key)

      if not post:
         self.error(404)
      elif post.user_id != str(self.user.key().id()):
         self.redirect('/invalid')
      else:
         self.render('edit-post.html', p=post)


   def post(self, post_id):
      subject = self.request.get('subject')
      content = self.request.get('content')

      if subject and content:
         key = db.Key.from_path('Post', int(post_id), parent=blog.blog_key())
         p = db.get(key)
         p.subject = subject
         p.content = content
         p.put()
         self.redirect('/blog/%s' % str(p.key().id()))
      else:
         self.render('newpost.html',
                     subject=subject,
                     content=content,
                     error_msg='Enter both subject and content, please!')



class DeletePostHandler(base.BaseHandler):
   """
   handles '/blog/delete/(\d+)' where the number is the post id
   delete the post of post_id
   """
   def get(self, post_id):
      if not self.user:
         self.redirect('/login')

      key = db.Key.from_path('Post', int(post_id), parent=blog.blog_key())
      post = db.get(key)

      if not post:
         self.error(404)
      elif post.user_id != str(self.user.key().id()):
         self.redirect('/invalid')
      else:
         post.delete()
         self.redirect('/blog')



class PostLikeHandler(base.BaseHandler):
   """
   handles '/blog/(like|dislike)/(\d+)/(\d+)' where the number is post_id
   and user_id of that post.
   """
   def get(self, up, post_id, user_id):
      if not self.user:
         self.redirect('/login')

      if user_id == str(self.user.key().id()):
         self.redirect('/invalid/2')
      elif like.Like.check_exist(post_id, str(self.user.key().id())):
         # check the post_id and user_id of the current user
         self.redirect('/invalid/4')
      else:
         lk = True if up == 'like' else False
         like.Like.add_like(post_id, user_id, lk)
         self.redirect('/blog')







