#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Data property. """

from google.appengine.ext import db

class apikey(db.Model):
  """ Volunteer basedata. """
  pkey = db.StringProperty()

class userdata(db.Model):
  """ Login ID/PWD 
      user id as a key_name """
  password = db.StringProperty()
