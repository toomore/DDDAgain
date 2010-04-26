#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import urlfetch

import urllib2,md5
import feedparser,datamodel


class readRss:
  def __init__(self,url):
    self.url = url;
    #self.result = urllib2.urlopen(url)
    self.result = urlfetch.fetch(url)
    #self.etree = feedparser.parse(self.result)
    self.etree = feedparser.parse(self.result.content)
    self.hcode = self.result.status_code
    self.headers = self.result.headers

############## webapp Models ###################
class MainPage(webapp.RequestHandler):
  def get(self):
    RR = readRss('http://twitter.com/statuses/user_timeline/12717952.rss')
    a = RR.etree

    self.response.out.write('Hello, webapp World!<br>')

    name = a.channel.title.split(' ')
    twies = datamodel.twies

    for b in a.entries:
      rsscon = (b.title[(len(name[2])+2):]).encode('utf-8')
      rsshash = md5.new()
      rsshash.update(rsscon)
      if twies.get_by_key_name(rsshash.hexdigest()):
        pass
      else:
        twies(key_name = rsshash.hexdigest(), content = rsscon.decode('utf-8'), posted = False).put()

      self.response.out.write( '%s - %s' % (rsshash.hexdigest(),rsscon) )
      self.response.out.write('<br>')

    self.response.out.write('<br>')

'''
class indata(webapp.RequestHandler):
  def get(self):

    ### Input the Plurk API
    #a = datamodel.apikey
    #a(pkey = 'xxx').put()

    ### Get the Plurk APl
    #q = a.all()
    #self.response.out.write(q[0].pkey)

    ### Input User ID/PWD
    #b = datamodel.userdata
    #b(key_name = 'xxx',password = 'xxx').put()
'''

############## main Models ###################
def main():
  """ Start up. """
  application = webapp.WSGIApplication(
                                      [
                                        ('/', MainPage)
                                      ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
