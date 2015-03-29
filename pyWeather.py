#!/usr/bin/python
import SensorReader, Displayer, QueueMultiplexer, ThingSpeak
from Queue import Queue
import sys

dataQueue=Queue(10)

sr=SensorReader.SensorReader(dataQueue)
qm=QueueMultiplexer.QueueMultiplexer(dataQueue)
d=Displayer.Displayer()
qm.add_listener(d)
if len(sys.argv)>1:
  ts=ThingSpeak.ThingSpeakUpdater(sys.argv[1])
  qm.add_listener(ts)
sr.start()
qm.start()
try:
  sr.join()
except:
  pass
sr.stop()
qm.stop()
d.stop()


