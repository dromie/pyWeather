#!/usr/bin/python
from threading import Thread
import time
import random
from Queue import Queue


class QueueMultiplexer(Thread):
  def __init__(self,queue):
    Thread.__init__(self)
    self.queue=queue
    self.listeners=[]
    self.stopped=False

  def stop(self):
    self.stopped=True

  def add_listener(self,listener):
    self.listeners.append(listener)

  def run(self):
    while not self.stopped:
      data = self.queue.get()
      for listener in self.listeners:
        listener.update(data)
      self.queue.task_done()



