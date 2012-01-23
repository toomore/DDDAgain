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

class plurkid(db.Model):
  """ Plurk user account """
  user = db.UserProperty(auto_current_user_add=True)
  uid = db.StringProperty()
  upwd = db.StringProperty()

class twies(db.Model):
  """ Save twitters
      unicode as a key_name """
  content = db.StringProperty()
  posted = db. BooleanProperty()
  datetime = db.DateTimeProperty(auto_now_add = True)
