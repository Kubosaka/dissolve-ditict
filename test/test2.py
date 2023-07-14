import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob

    
img = Image.open("./frame2/000001.jpg").convert('L')
width, height = img.size
print(width)
print(height)
image_array = np.zeros((width, height), dtype=int)
for x in range(width):
    for y in range(height):
        image_array[x][y] = img.getpixel((x, y))
print(image_array)

# 画像をリサイズする
img_resized = img.resize((width//16, height//16))
width, height = img_resized.size
print(width)
print(height)

image_array2 = np.zeros((width, height), dtype=int)
for x in range(height):
    for y in range(width):
        image_array2[y][x] = img_resized.getpixel((y, x))
print(image_array2)

a = img_resized.getdata()
b = np.array(a)
width, height = img_resized.size
b= b.reshape(height, width)
b = np.transpose(b)
print(img_resized.size)
print(b)

