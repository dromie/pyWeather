#!/usr/bin/python

import Adafruit_BMP.BMP085 as BMP085
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import Image
import ImageFont
import ImageDraw

debug=False

sensor = BMP085.BMP085()
display = Adafruit_SSD1306.SSD1306_128_64(rst=24)

display.begin()
width = display.width
height = display.height
font = ImageFont.truetype("arial.ttf",64)
iteration=0

def composeString(temp,press):
  t=time.strftime("%H:%M")
  text="%s %2.1f%s %2.0f hPa"%(t,temp,unichr(176)+"C",press/100.0)
  return text

def printCalibration(bmp):
  if debug:
    print "cal_AC1=",bmp.cal_AC1
    print "cal_AC2=",bmp.cal_AC2
    print "cal_AC3=",bmp.cal_AC3
    print "cal_AC4=",bmp.cal_AC4
    print "cal_AC5=",bmp.cal_AC5
    print "cal_AC6=",bmp.cal_AC6
    print "cal_B1=",bmp.cal_B1 
    print "cal_B2=",bmp.cal_B2 
    print "cal_MB=",bmp.cal_MB 
    print "cal_MC=",bmp.cal_MC 
    print "cal_MD=",bmp.cal_MD 


def printDebug(t,p,rt,rp):
  print time.strftime("%Y-%m-%d %H:%M:%S")," ",
  print rt,rp,t,p


def readSensor(bmp):
   t = bmp.read_temperature()
   p = bmp.read_pressure()
   if debug:
     rt = bmp.read_raw_temp()
     rp = bmp.read_raw_pressure()
     printDebug(t,p,rt,rp)
   return t,p+1700



printCalibration(sensor)
calibrationText=composeString(-99.99,999999)
w,h = font.getsize(calibrationText)
wrapspace=font.getsize(" ")[0]
image = Image.new('1', (w+width+wrapspace, height))
draw = ImageDraw.Draw(image)
while True:
  if iteration%400 == 0:
   temp,press = readSensor(sensor)
   text = composeString(temp,press)
   draw.rectangle((0,0,w+width,height), outline=0, fill=0)
   w,h = font.getsize(text)
   draw.text((0,-1),text,font=font,fill=255)
   image.paste(image.crop((0,0,width,height)),(w+wrapspace,0,w+width+wrapspace,height))
  display.clear()
  offset=iteration%w
  display.image(image.crop((offset,0,offset+width,height)))

#  showPressure(sensor.read_pressure(),iteration)
#  showTemperature(sensor.read_temperature())
#  display.image(image)
  display.display()
  iteration+=5


