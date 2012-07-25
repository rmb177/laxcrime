"""
Copyright (c) 2012 Brubaker LLC. All rights reserved.
"""

import json
import urllib
import webapp2

from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import db

from models.IncidentReport import IncidentReport


class RetrieveIncidentLatLong(webapp2.RequestHandler):

   def post(self):
      """
      Fetches lat/long coordinates for the given incident report type
      """
      incidentId = int(self.request.get('id'))
      report = IncidentReport.get_by_id(incidentId)
      if None != report:
         params = urllib.urlencode(
         {
            'address' : '%s %s WI' %(report.address, report.city.name),
            'sensor' : 'true' 
         })
         url = "http://maps.googleapis.com/maps/api/geocode/json?%s" %(params)
         result = urlfetch.fetch(url)
         if 200 == result.status_code:
            try:
               llResults = json.loads(result.content)['results'][0]['geometry']['location']
               report.latLong = db.GeoPt(llResults['lat'], llResults['lng'])
               report.save()
            except:
               mail.send_mail(sender="LaxCrime <ryan.brubaker@gmail.com>",
                to="Ryan Brubaker <ryan.brubaker@gmail.com>",
                subject="Error getting lat long",
                body="""
                     Error trying to retrieve lat/long for incident report with id: %d
                     \n\n
                     %s
                  """ %(incidentId, result.content))
               
         else:
            mail.send_mail(sender="LaxCrime <ryan.brubaker@gmail.com>",
             to="Ryan Brubaker <ryan.brubaker@gmail.com>",
             subject="Error getting lat long",
             body="""
                     Error trying to retrieve lat/long for incident report with id: %d
                     \n\n
                     %s
                  """ %(incidentId, result.content))
         #
      #
   #   
#


app = webapp2.WSGIApplication([('/retrieve-incident-latlong', RetrieveIncidentLatLong)], debug=True)
