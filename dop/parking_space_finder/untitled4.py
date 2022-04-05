# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 12:31:16 2022

@author: user
"""

from PIL import Image, ImageFilter
import pytesseract
pytesseract.pytesseract.tesseract_cmd = 'D:/tesseract/tesseract.exe'

img = Image.open('bc2.jpg')
img2 = img.filter(ImageFilter.BLUR)
pixels = img2.load()
width, height = img2.size
x_ = []
y_ = []
for x in range(width):
    for y in range(height):
        if pixels[x, y] == (255, 255, 255):
            x_.append(x)
            y_.append(y)

img = img.crop((min(x_), min(y_),  max(x_), max(y_)))
text = pytesseract.image_to_string(img, lang='eng', config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
print(text)

