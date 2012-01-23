#!/usr/bin/env python
# -*- coding: utf-8 -*-

import plurklib
from datamodel import plurkid
from datamodel import apikey

PLURK_KEY = apikey.all()[0].pkey

def posttoplurk(umail,say):
  u = plurkid.gql("where user = USER('%s')" % umail)
  for i in u:
    p = plurklib.PlurkAPI(PLURK_KEY)
    p.login(i.uid,i.upwd)
    p.plurkAdd(say.encode('utf-8'))
    p.logout()
