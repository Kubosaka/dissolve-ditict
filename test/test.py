import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob


image_arrays= np.empty((0))
print(image_arrays)
print(len(image_arrays))
files = glob.glob("./frame2/*")
for file in files:
    print(file)
    img = Image.open(file).convert('L')
    width, height = img.size
    image_array = np.zeros((width, height), dtype=int)
    for x in range(width):
        for y in range(height):
            image_array[x][y] = img.getpixel((x, y))
    image_arrays = np.append(image_arrays, image_array)
    print(image_array.shape)
    print(image_array)
    

print(image_arrays.shape)
print(image_arrays)
