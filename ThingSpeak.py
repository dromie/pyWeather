#!/usr/bin/python

import requests


class ThingSpeakUpdater:
  def __init__(self,apikey):
    self.apikey=apikey
    self.data=(0,0)
  
  def update(self,data):
    dc=(data[0],data[1]/100.0)
    if abs(self.data[0]-dc[0])>1 or abs(self.data[1]-dc[1])>1:
      self.data=dc
      URL="https://api.thingspeak.com/update?api_key=%s"%(self.apikey)
      for i in range(len(dc)):
        field="field%d"%(i+1)
        URL=URL+"&%s=%s"%(field,str(dc[i]))
      print URL
      result=requests.get(URL)
      print result
      if result.status_code<200 or result.status_code>=300:
        print "Request failed (%d) '%s'"%(result.status_code,result.content)

