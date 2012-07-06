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
      incidentReports.fetch(None)
       
      self.response.headers['Content-Type'] = 'application/json'
      
      self.response.out.write(''.join(['[', ','.join([incidentReport.asJson() for incidentReport in incidentReports]), ']']))
      #return '[' + str(',').join([incidentReport.asJson() for incidentReport in incidentReports]) + ''
      #return ''.join(['[', ','.join([incidentReport.asJson() for incidentReport in incidentReports]), ']'])
      #jsonRet = "[" 
      #incidentReports = IncidentReport.all().fetch(None)
      #for incidentReport in incidentReports:
      #   jsonRet += incidentReport.asJson()
      #   jsonRet += ","
      #jsonRet += "]"
      #self.response.out.write(jsonRet)
        #return ''.join([`num` for num in xrange(loop_count)])

      #def method6():
#   #
#


app = webapp2.WSGIApplication([('/get_incident_reports', GetIncidentReports)], debug=True)
