"""
Copyright (c) 2012 Brubaker LLC. All rights reserved.
"""

import logging
import os
import re
import webapp2
from datetime import datetime

from google.appengine.ext.webapp import template

from models.City import City
from models.IncidentReport import IncidentReport
from models.IncidentType import IncidentType


log = logging.getLogger(__file__)
log.setLevel(logging.DEBUG)

class UploadInformationHandler(webapp2.RequestHandler):

   def get(self):
      """
      Displays the main page of the application
      """
      path = os.path.join(os.path.dirname(__file__), '../pages/upload_information.html')
      self.response.out.write(template.render(path, {}))
   #
   
   def post(self):
      """
      Parses a list of police/fire calls and fires off a task for each one
      """
      incidentType = None
      incidentTypeNames = [incident.name.lower() for incident in IncidentType.all()]
      
      city = None
      cityNames = [city.name.lower() for city in City.all()]
      
      lines = self.request.get('report').split('\n')
      lineNum = 0
      
      startDate = None
      endDate = None
      
      for strippedLine in [line.strip() for line in lines if line.strip() != '']:
         try:
            if 0 == lineNum:
               startDate = strippedLine
            elif 1 == lineNum:
               endDate = strippedLine
            else:
               if strippedLine.lower() in incidentTypeNames:
                  incidentType = IncidentType.all().filter('name =', strippedLine.lower()).get()
                  city = None
               elif strippedLine.lower() in cityNames:
                  city = City.all().filter('name =', strippedLine.lower()).get()
               else:
                  match = re.search('^[0-9]+', strippedLine)
                  lineItemTokens = strippedLine.split(',')
                  if None != match and 3 == len(lineItemTokens):
                     timeToken = lineItemTokens[0]
                     descToken = lineItemTokens[1].title()
                     addressToken = lineItemTokens[2].title()
                     
                     # Check for date, anything on or after 3 pm is the start date
                     # anything on or after 12 am is the end date
                     dateString = endDate
                     if int(match.group(0)) >= 3 and int(match.group(0)) < 12 and -1 != timeToken.find('p.m.'):
                        dateString = startDate
                     
                     dateOfIncident = datetime.strptime(
                      '%s %s' %(dateString, timeToken.replace('a.m.', 'AM').replace('p.m.', 'PM')), 
                      '%m/%d/%Y %I:%M %p')
                                                                           
                     # We've parsed out all informaton so create a record...just bail on this record
                     # if we're in a bad state
                     assert(None != incidentType and None != city)
                     incidentReport = IncidentReport(
                      incidentType = incidentType,
                      description = descToken,
                      time = dateOfIncident,
                      city = city,
                      address = addressToken)
                     incidentReport.save()
                  #
                  else:
                     incidentType = None
                     city = None
                     raise Exception('Unrecognized line')
                  #
               #
            #
         #  
         except (Exception, AssertionError) as e:
            if isinstance(e, AssertionError):
               e = 'Incident type or city was null.'
            self.response.out.write("Error processing line: %s <br />" %(strippedLine))
            self.response.out.write('<div style="margin:5px;">%s</div>' %(str(e)))
            self.response.out.write('<br />')
         #
         lineNum += 1
      #
   #
#


app = webapp2.WSGIApplication([('/upload_information', UploadInformationHandler)], debug=True)
