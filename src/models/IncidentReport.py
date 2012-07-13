"""
Copyright (c) 2012 Brubaker LLC. All rights reserved.
"""

from datetime import datetime

from google.appengine.ext import db
from models.City import City
from models.IncidentType import IncidentType


class IncidentReport(db.Model):
   incidentType = db.ReferenceProperty(IncidentType)
   description = db.TextProperty()
   time = db.DateTimeProperty()
   city = db.ReferenceProperty(City)
   address = db.TextProperty()
   latLong = db.GeoPtProperty()
   
   
   def asJson(self):
      jsonStr = '{"type:%s,"}' %(self.incidentType.name)
      return '{"type":"%s","time":"%s","description":"%s","address":"%s","lat":"%s","long":"%s"}' %(
       self.incidentType.name,
       datetime.strftime(self.time, '%m/%d/%Y %I:%M %p'),
       self.description,
       self.address,
       self.latLong.lat if self.latLong else '',
       self.latLong.lon if self.latLong else '')


