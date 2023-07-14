import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob

image_arrays= np.empty((0))
files = glob.glob("./frames/*")
files = sorted(files)
count = 0
for file in files:
    print(file)
    #画像open(グレースケール)
    img = Image.open(file).convert('L')
    width, height = img.size
    #画像をリサイズ(縦横1/16)
    img_resized = img.resize((width//16, height//16))
    #画像データ取得
    imgData = img_resized.getdata()
    width, height = img_resized.size
    imgData = np.array(imgData)
    image_arrays = np.append(image_arrays, imgData)
    count += 1

print()
# 3次元配列に変換
image_arrays = image_arrays.reshape(count, height, width)
print(image_arrays.shape)
print(image_arrays)

