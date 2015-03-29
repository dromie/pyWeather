#!/usr/bin/python
from threading import Thread
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Image
import ImageFont
import ImageDraw

def _composeString(temp,press):
  t=time.strftime("%H:%M")
  text="%s %2.1f%s %2.0f hPa"%(t,temp,unichr(176)+"C",press/100.0)
  return text

class Displayer(Thread):
  def __init__(self):
    Thread.__init__(self)
    self.display = Adafruit_SSD1306.SSD1306_128_64(rst=24)
    self.display.begin()
    self.stopped=False
    self.data=None

  def update(self,data):
    shouldStart=self.data==None
    self.data=data
    if shouldStart:
      self.start()

  def run(self):
    iteration=0
    width = self.display.width
    height = self.display.height
    font = ImageFont.truetype("arial.ttf",64)
    calibrationText=_composeString(-99.99,999999)
    w,h = font.getsize(calibrationText)
    wrapspace=font.getsize(" ")[0]
    image = Image.new('1', (w+width+wrapspace, height))
    draw = ImageDraw.Draw(image)
    while True:
      if iteration%400 == 0:
        text = _composeString(self.data[0],self.data[1])
        draw.rectangle((0,0,w+width,height), outline=0, fill=0)
        w,h = font.getsize(text)
        draw.text((0,-1),text,font=font,fill=255)
        image.paste(image.crop((0,0,width,height)),(w+wrapspace,0,w+width+wrapspace,height))
      self.display.clear()
      offset=iteration%w
      self.display.image(image.crop((offset,0,offset+width,height)))
      self.display.display()
      iteration+=5
      time.sleep(1/100)


