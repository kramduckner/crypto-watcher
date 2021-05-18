from lcd_1in44 import LCD
from gpiozero import Button
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Dict, Callable
import json
import time
import datetime
import pytz
import math
import requests
import threading
import crypto_utils
import globals

lcd = LCD()
lcd.LCD_Init()
lcd.LCD_Clear()
img = Image.new("RGB", (lcd.width, lcd.height))
font = ImageFont.truetype("OpenSans-Regular.ttf", 20)
font_small = ImageFont.truetype("OpenSans-Regular.ttf", 16)
font_tiny = ImageFont.truetype("OpenSans-Regular.ttf", 12)
timezone = pytz.timezone("UTC")

class priceUpdaterThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      
   def run(self):
       while True:
           print('fetching')
           price, diff, ohlc = crypto_utils.fetch_crypto_data(globals.symbols_to_ticker[globals.symbols[globals.selected_symbol_index]])
           draw = ImageDraw.Draw(img)
           draw.rectangle((0, 0, lcd.width, lcd.height), fill=(0, 0, 0, 0))
           draw.text((8, 5), text="{} ${}".format(globals.symbols[globals.selected_symbol_index], 
                                                  crypto_utils.price_to_str(price)), font=font_small, fill=(255, 255, 255, 255))
           diff_symbol = ""
           diff_color = (255, 255, 255, 255)
           if diff > 0:
               diff_symbol = "+"
               diff_color = (55, 255, 55, 255)
           if diff < 0:
               diff_color = (255, 55, 55, 255)
               draw.text((8, 30), text="{}{}$".format(diff_symbol,
                                                      crypto_utils.price_to_str(diff)), font=font_small, fill=diff_color)
               draw.text((6, 106), text=datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S"),
                         font=font_tiny, fill=(200, 200, 200, 255))
               crypto_utils.render_ohlc_data(ohlc, draw)
               lcd.LCD_ShowImage(img)
               time.sleep(60)


