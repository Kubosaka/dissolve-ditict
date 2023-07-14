import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob

    
img = Image.open("./frame2/000001.jpg").convert('L')
width, height = img.size

# 画像をリサイズする
img_resized = img.resize((width//16, height//16))

imgData = img_resized.getdata()
width, height = img_resized.size
imgData = np.transpose(np.array(imgData).reshape(height, width))

print(img_resized.size)
print(imgData)

image_arrays= np.empty((0))
files = glob.glob("./frame2/*")
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

print()
# 3次元配列に変換
image_arrays = image_arrays.reshape(2, height, width)
print(image_arrays.shape)
print(image_arrays)

# 画像出力
a=list(image_arrays[1].reshape(3600))
a = list(map(int, a))
print(a)
newImg = Image.new("L", (80,45), color=0)
newImg.putdata(a)
newImg.show()
