"""
Copyright (c) 2012 Brubaker LLC. All rights reserved.
"""

import os
import webapp2

from models.City import City
from models.IncidentType import IncidentType


class CreateDefaultInformationHandler(webapp2.RequestHandler):

   def get(self):
      """
      Create default data
      """
      city = City(name='la crosse')
      city.save()
      self.response.out.write('Created la crosse<br/>')

      city = City(name='onalaska')
      city.save()
      self.response.out.write('Created onalaska<br/>')

      city = City(name='holmen')
      city.save()
      self.response.out.write('Created holmen<br/>')

      city = City(name='west salem')
      city.save()
      self.response.out.write('Created west salem<br/>')

      city = City(name='bangor')
      city.save()
      self.response.out.write('Created bangor<br/>')

      city = City(name='town of campbell')
      city.save()
      self.response.out.write('Created town of csampbell<br/>')

      
      aType = IncidentType(name="police calls")
      aType.save()
      self.response.out.write('Created police calls type<br/>')

      aType = IncidentType(name="fire calls")
      aType.save()
      self.response.out.write('Created fire calls type<br/>')
#

app = webapp2.WSGIApplication([('/create_default_information', CreateDefaultInformationHandler)], debug=True)
