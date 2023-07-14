import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import glob
import pandas as pd


image_arrays= np.empty((0))
files = sorted(glob.glob("./frames/*"))

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

# 3次元配列に変換
image_arrays = image_arrays.reshape(count, height, width)

# 各フレームの画素の差分の配列
d_image_arrays= np.empty((0))

# 各フレームの画素の差分の配列
r_imgs = np.empty((0))

for i in range(1,len(image_arrays)):
    # 現在フレームと前フレームの差分
    d_img = image_arrays[i]-image_arrays[i-1]
    d_image_arrays = np.append(d_image_arrays, d_img)
    d_image_arrays = d_image_arrays.reshape(i, height, width)

    #現フレームと前フレームの差分の比が正になる画素の全体に占める割合
    if i>1:
        r_img = d_img/d_image_arrays[i-2]
        # print("{0}と{1}の差".format(i,i-1))
        # print(d_img)
        # print("{0}と{1}の差".format(i-1,i-2))
        # print(d_image_arrays[i-2])
        # print("差分の比")
        # print(r_img)
        r_img= np.floor(r_img * 10) / 10
        r_img[np.isnan(r_img)] = 0
        r_img[np.isinf(r_img)] = 1
        count = np.count_nonzero(0<r_img)/(width*height)
        r_imgs = np.append(r_imgs, count)
   
# pandasに変換(データの平滑化を行うため)
df = pd.Series(r_imgs)
md = 3
# メディアンフィルタ
df = df.rolling(md, center=True).mean()
# リストに変換
r_imgs = df.values.tolist()


# フィルタによって生じたNaNを除去
r_imgs=r_imgs[int((md-1)/2):int(-(md-1)/2)]


y_max = 0.1
if np.nanmax(r_imgs)<=0.5:
    y_max = 0.5
else:
    y_max = np.nanmax(r_imgs)+0.1

X = np.arange(0,len(r_imgs))
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111) #...2
ax.plot(X, r_imgs, marker='o', markersize=3)
ax.set_xlabel('frame number', fontsize=16)
ax.set_ylabel('Feature value', fontsize=16)

print(len(r_imgs))
print(r_imgs)
print(np.median(r_imgs))
print(np.min(r_imgs))
plt.xlim(-1, len(r_imgs)+1)
plt.ylim(0, y_max)
plt.title("Dissolve detection", fontsize=18)
plt.show()
