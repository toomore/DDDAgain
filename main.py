#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.api.taskqueue import Task
from google.appengine.api import urlfetch
import simplejson as json
import urllib2,md5
#import feedparser,datamodel
import plurklib
from datamodel import plurkid
from datamodel import apikey
import snspost

class readRss:
  def __init__(self,url):
    self.url = url;
    #self.result = urllib2.urlopen(url)
    self.result = urlfetch.fetch(url)
    #self.etree = feedparser.parse(self.result)
    self.etree = feedparser.parse(self.result.content)
    self.hcode = self.result.status_code
    self.headers = self.result.headers

class index(webapp.RequestHandler):
  def get(self):
    op = """
    User: %s
    <form action="/" method="POST">
      <textarea name="say"></textarea><br>
      <input type="submit">
    </form>
""" % users.get_current_user().nickname()
    self.response.out.write(op)
    u = plurkid.gql("where user = USER('%s')" % users.get_current_user().email())
    for i in u:
      p = plurklib.PlurkAPI(apikey.all()[0].pkey)
      rp = p.login(i.uid,i.upwd)
      for k in rp['plurks']:
        self.response.out.write(u'%s<hr>' % k.keys())
        self.response.out.write(u'%s - %s<hr>' % (k['owner_id'],k['content']))
      p.logout()

  def post(self):
    Task(url='/taskpostplurk',
          params={'say':self.request.get('say'),
                  'umail':users.get_current_user().email()}
        ).add()
    self.redirect("/")

class taskpostplurk(webapp.RequestHandler):
  def post(self):
    snspost.posttoplurk(self.request.get('umail'),self.request.get('say'))

class addplurkacc(webapp.RequestHandler):
  def get(self):
    op = """
    <form action="/addplurkacc" method="POST">
      ID\t<input name="id"><br>
      PWD\t<input name="pwd"><br>
      <input type="submit">
    </form>
"""
    self.response.out.write(op)

  def post(self):
    plurkid(uid=self.request.get('id'), upwd=self.request.get('pwd')).put()
    self.redirect("/")

############## webapp Models ###################
##### OLD #####
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
                                        ('/', index),
                                        ('/addplurkacc', addplurkacc),
                                        ('/taskpostplurk', taskpostplurk)
                                      ],debug=True)
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
