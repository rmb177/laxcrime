"""
Copyright (c) 2012 Brubaker LLC. All rights reserved.
"""

from google.appengine.ext import db


class IncidentType(db.Model):
   name = db.StringProperty()


