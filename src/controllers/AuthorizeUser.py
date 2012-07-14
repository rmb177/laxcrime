"""
Copyright (c) 2012 Brubaker LLC. All rights reserved.
"""

import webapp2


class AuthorizeUser(webapp2.RequestHandler):

   def get(self):
      """
      Checks password submitted by user. Just have a simple form here for demo for the tribune.
      Eventually this will go away so nothing fancy here.
      """
      password = self.request.get('password')
      if password == 'l@xcr1me':
         self.response.out.write('true')
      else:
         self.response.out.write('false')
   #
#


app = webapp2.WSGIApplication([('/authorize_user', AuthorizeUser)], debug=True)
