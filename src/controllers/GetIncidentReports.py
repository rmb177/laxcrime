"""
Copyright (c) 2012 Brubaker LLC. All rights reserved.
"""

import webapp2
from datetime import datetime
from models.IncidentReport import IncidentReport


class GetIncidentReports(webapp2.RequestHandler):

   def get(self):
      """
      Displays a form to upload a day's worth of incident reports
      """
      date = self.request.get('date')
      incidentReports = IncidentReport.all()
      incidentReports.filter("time >= ", datetime.strptime('%s 12:00 AM' %(date), '%m/%d/%Y %I:%M %p'))
      incidentReports.filter("time <= ", datetime.strptime('%s 11:59 PM' %(date), '%m/%d/%Y %I:%M %p'))
      results = incidentReports.run(limit=None)
      
      self.response.headers['Content-Type'] = 'application/json'
      self.response.out.write(''.join(['[', ','.join([result.asJson() for result in results]), ']']))
   #
#


app = webapp2.WSGIApplication([('/get_incident_reports', GetIncidentReports)], debug=True)
