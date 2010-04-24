#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from google.appengine.api import urlfetch

import feedparser,urllib2,md5


class readRss:
  def __init__(self,url):
    self.url = url;
    self.result = urllib2.urlopen(url)
    self.etree = feedparser.parse(self.result)

class MainPage(webapp.RequestHandler):
  def get(self):
    a = readRss('http://twitter.com/statuses/user_timeline/12717952.rss').etree
    #a = readRss('http://feedparser.org/docs/examples/rss20.xml').etree

    self.response.out.write('Hello, webapp World!<br>')

    name = a.channel.title.split(' ')

    for b in a.entries:
      rsscon = (b.title[(len(name[2])+2):]).encode('utf-8')
      rsshash = md5.new()
      rsshash.update(rsscon)

      self.response.out.write( '%s - %s' % (rsshash.hexdigest(),rsscon) )
      self.response.out.write('<br>')


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
