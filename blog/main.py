#!/usr/bin/env python
#
# Copyright 2016 Nengyun Zhang
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

import webapp2

from handlers import mainpage, blog, user, other

app = webapp2.WSGIApplication([
   ('/', mainpage.MainPageHandler),
   ('/blog', blog.BlogFrontPageHandler),
   ('/blog/newpost', blog.AddNewPostPageHandler),
   ('/blog/(\d+)', blog.PermalinkPageHandler),
   ('/blog/edit/(\d+)', blog.EditPostPageHandler),
   ('/blog/delete/(\d+)', blog.DeletePostHandler),
   ('/blog/(like|dislike)/(\d+)/(\d+)', blog.PostLikeHandler),
   ('/blog/myblog', blog.MyBlogPageHandler),
   ('/blog/newcomment/(\d+)/(\d+)', blog.NewCommentPageHandler),
   ('/blog/comment/delete/(\d+)', blog.DeleteCommentHandler),
   ('/blog/comment/edit/(\d+)', blog.EditCommentPageHandler),
   ('/signup', user.SignupPageHandler),
   ('/login', user.LoginPageHandler),
   ('/logout', user.LogoutHandler),
   ('/invalid/(\d+)', other.InvalidPageHandler)
   ], debug=True)
























