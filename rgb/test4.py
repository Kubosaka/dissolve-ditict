import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import math
import glob
import pandas as pd



# 256を分割する変数
class_x = 32
# class_x = 64

# 色ごとに256/classX分割する関数
def classRGB(x):
    return np.floor(x/class_x)

image_arrays= np.empty((0))
path = "./frames3/*"
files = sorted(glob.glob(path))

count = 0
for file in files:
    #画像open
    img = Image.open(file)
    width, height = img.size
    #画像データ取得
    #データのリサイズ(大きすぎるため)
    img = img.resize((width//4, height//4))
    imgData = np.array(img)
    image_arrays = np.append(image_arrays, imgData)
    count += 1

width, height = img.size

# 4次元配列に変換
image_arrays = image_arrays.reshape(count, height, width, 3)

# 画像フレームを縦横4分割
block_w = int(width/4)
block_h = int(height/4)

# rgbの色を分割する変数
classX = int(256/class_x)


# 各フレームの評価値リスト
value_list = np.empty(0)

# 各フレームの処理
for ix in range(1,len(image_arrays)):
    img1 = image_arrays[ix-1]

    img2 = image_arrays[ix]

    # 各フレームの評価値リスト
    x2_list = np.empty(0)

    for ih in range(block_h,height+1,block_h):
        for iw in range(block_w, width+1,block_w):
            # block
            blockImage=img1[ih-block_h:ih, iw-block_w:iw]
            blockImage2=img2[ih-block_h:ih, iw-block_w:iw]
            r = classRGB(blockImage[:,:,0])
            r2 = classRGB(blockImage2[:,:,0])
            g = classRGB(blockImage[:,:,1])
            g2 = classRGB(blockImage2[:,:,1])
            b = classRGB(blockImage[:,:,2])
            b2 = classRGB(blockImage2[:,:,2])
            # 色の要素数を保存するリスト
            imgRCount=np.zeros((2,classX))
            imgGCount=np.zeros((2,classX))
            imgBCount=np.zeros((2,classX))

            # 色をカウント
            for i in range(classX):
                imgRCount[0][i] = np.count_nonzero(r==i)
                imgRCount[1][i] = np.count_nonzero(r2==i)
                imgGCount[0][i] = np.count_nonzero(g==i)
                imgGCount[1][i] = np.count_nonzero(g2==i)
                imgBCount[0][i] = np.count_nonzero(b==i)
                imgBCount[1][i] = np.count_nonzero(b2==i)

            # 0による除算防止
            imgRCount[imgRCount == 0] = 1
            imgGCount[imgGCount == 0] = 1
            imgBCount[imgBCount == 0] = 1

            # 評価値
            x2R=0
            x2G=0
            x2B=0

            for i in range(classX):
                eiR = imgRCount[0][i]
                oiR = imgRCount[1][i]
                eiG = imgGCount[0][i]
                oiG = imgGCount[1][i]
                eiB = imgBCount[0][i]
                oiB = imgBCount[1][i]

                x2R += (oiR-eiR)**2/eiR
                x2G += (oiG-eiG)**2/eiG
                x2B += (oiB-eiB)**2/eiB

            x2_list=np.append(x2_list,x2R+x2G+x2B)

    # x2_list = x2_list.reshape(16,3)
    x2_list = np.sort(x2_list)
    value = np.sum(x2_list[:10])
    value_list = np.append(value_list, value)

y_max = 0.1
if np.nanmax(value_list)<=5000:
    y_max = 5000
else:
    y_max = np.nanmax(value_list)+2000

md=3
# pandasに変換(データの平滑化を行うため)
df = pd.Series(value_list)
# メディアンフィルタ
df = df.rolling(3, center=True).median()
# リストに変換
value_list = df.values.tolist()
value_list=value_list[int((md-1)/2):int(-(md-1)/2)]
print(len(value_list))

X = np.arange(0,len(value_list))
fig = plt.figure(figsize=(12, 8))
# Figure内にAxesを追加()
ax = fig.add_subplot(111) #...2
ax.plot(X, value_list, marker='o', markersize=3)
ax.set_xlabel('frame number', fontsize=16)
ax.set_ylabel('Feature value', fontsize=16)
plt.xlim(-1, len(value_list)+1)
plt.ylim(0, y_max)
plt.title("Scene change detection Graph", fontsize=18)
plt.show()

