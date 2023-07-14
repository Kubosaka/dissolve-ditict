import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob

image_arrays= np.empty((0))
files = sorted(glob.glob("./frames4/*"))

count = 0
for file in files:
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
# print(image_arrays.shape)
# print(image_arrays)

# 各フレームの画素の差分の配列
d_image_arrays= np.empty((0))
r_imgs = np.empty((0))
for i in range(len(image_arrays)-1):
    # 現在フレームと前フレームの差分(絶対値)
    d_img = image_arrays[i+1]-image_arrays[i]
    d_image_arrays = np.append(d_image_arrays, d_img)
    d_image_arrays = d_image_arrays.reshape(i+1, height, width)
    #現フレームと前フレームの差分(各画素)の比が正になる画素の全体に占める割合
    print(d_image_arrays[i-1])
    r_img = (np.count_nonzero(d_image_arrays[i-1] < d_img))/(height*width)
    r_imgs = np.append(r_imgs,r_img)


d_image_arrays = d_image_arrays.reshape(count-1, height, width)
print(d_image_arrays.shape)
print(d_image_arrays[10:30])
print(r_imgs.shape)
print(r_imgs)

X = np.arange(0,len(r_imgs))
fig = plt.figure(figsize=(12, 8))
# Figure内にAxesを追加()
ax = fig.add_subplot(111) #...2
ax.plot(X, r_imgs, label="test")

plt.show()
