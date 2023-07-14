import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob

image_arrays= np.empty((0))
files = sorted(glob.glob("./frames/*"))

# メディアンフィルタ
def median(r_image):
    height, width =r_image.shape
    new_img = np.zeros((height-2,width-2))
    for y in range(1, height-1):
        for x in range(1, width-1):
            a = np.array([r_image[y-1][x-1],r_image[y-1][x],r_image[y-1][x+1],r_image[y][x-1],r_image[y][x],r_image[y][x+1],r_image[y+1][x-1],r_image[y+1][x],r_image[y+1][x+1]])
            a = np.sort(a)
            new_img[y-1,x-1] = a[4]
    return new_img

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

# 各フレームの画素の差分の配列
r_imgs = np.empty((0))
for i in range(1,len(image_arrays)):
    # 現在フレームと前フレームの差分
    d_img = image_arrays[i]-image_arrays[i-1]
    d_img[d_img==0] = 0.00001
    print(i)
    d_image_arrays = np.append(d_image_arrays, d_img)
    d_image_arrays = d_image_arrays.reshape(i, height, width)
    print(d_img)
    print()
    #現フレームと前フレームの差分の比が正になる画素の全体に占める割合
    if i>1:
        print(d_image_arrays[i-2])
        print()
        r_img = d_img/d_image_arrays[i-2]
        print(r_img)
        r_img= np.floor(r_img * 10) / 10
        md_r_img=median(r_img)
        count = np.count_nonzero(1<md_r_img)
        r_imgs = np.append(r_imgs, count)
    


print(r_imgs)
X = np.arange(0,len(r_imgs))
fig = plt.figure(figsize=(12, 8))
# Figure内にAxesを追加()
ax = fig.add_subplot(111) #...2
ax.plot(X, r_imgs, label="test")

plt.show()


# # 整形
# d_image_arrays = d_image_arrays.reshape(count-1, height, width)

# X = np.arange(0,len(r_imgs))
# fig = plt.figure(figsize=(12, 8))
# # Figure内にAxesを追加()
# ax = fig.add_subplot(111) #...2
# ax.plot(X, r_imgs, label="test")

# plt.show()
