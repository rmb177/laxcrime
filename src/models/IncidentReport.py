"""
Copyright (c) 2012 Brubaker LLC. All rights reserved.
"""

import datetime

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


