#!/usr/bin/python

import Adafruit_BMP.BMP085 as BMP085
import time
from threading import Thread
from Queue import Queue

class SensorReader(Thread):
  def __init__(self,queue):
    Thread.__init__(self)
    self.sensor = BMP085.BMP085()
    self.queue=queue
    self.stopped=False
  
  def run(self):
    while not self.stopped:
      t = self.sensor.read_temperature()
      p = self.sensor.read_pressure()+1700
      self.queue.put((t,p))
      time.sleep(5)

  def stop(self):
    self.stopped=True

