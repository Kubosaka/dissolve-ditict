import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
import math
import glob
import pandas as pd
import scipy as sp
import scipy.stats


# 256を分割する変数
class_x = 32
# 色ごとに4分割する関数
def classRGB(x):
    return np.floor(x/class_x)

image_arrays= np.empty((0))
files = sorted(glob.glob("./testframe/*"))

count = 0
for file in files:
    #画像open(グレースケール)
    img = Image.open(file)
    width, height = img.size
    #画像をリサイズ(縦横1/16)
    #画像データ取得
    imgData = np.array(img)
    image_arrays = np.append(image_arrays, imgData)
    count += 1


# 4次元配列に変換
image_arrays = image_arrays.reshape(count, height, width, 3)

# 画像フレームを縦横4分割
block_w = int(width/4)
block_h = int(height/4)

# 16分割のうちのブロック
blockImage=image_arrays[0,0:block_h,0:block_w]
blockImage2=image_arrays[1,0:block_h,0:block_w]

# # rgb
# print(blockImage)
# # rだけ
# print("R")
# print(classRGB(blockImage[:,:,0]))

r = classRGB(blockImage[:,:,0])
r2 = classRGB(blockImage2[:,:,0])
g = classRGB(blockImage[:,:,1])
g2 = classRGB(blockImage2[:,:,1])
b = classRGB(blockImage[:,:,2])
b2 = classRGB(blockImage2[:,:,2])

classX = int(256/class_x)
imgRCount=np.zeros(classX)
imgRCount2=np.zeros(classX)
imgGCount=np.zeros(classX)
imgGCount2=np.zeros(classX)
imgBCount=np.zeros(classX)
imgBCount2=np.zeros(classX)

for i in range(classX):
    imgRCount[i] = np.count_nonzero(r==i)
    imgRCount2[i] = np.count_nonzero(r2==i)
    imgGCount[i] = np.count_nonzero(g==i)
    imgGCount2[i] = np.count_nonzero(g2==i)
    imgBCount[i] = np.count_nonzero(b==i)
    imgBCount2[i] = np.count_nonzero(b2==i)

# 1枚目と2枚目のフレームの差分の2次元リストに
imgRCount= np.append(imgRCount, imgRCount2).reshape(2, classX)
imgGCount= np.append(imgGCount, imgGCount2).reshape(2, classX)
imgBCount= np.append(imgBCount, imgBCount2).reshape(2, classX)

x = np.array([[10, 10, 20], [20, 20, 20]])

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
    kaiR = (oiR-eiR)**2/eiR
    kaiG = (oiG-eiG)**2/eiG
    kaiB = (oiB-eiB)**2/eiB
    x2R += kaiR
    x2G += kaiG
    x2B += kaiB
print("x2R={0}".format(x2R))
print("x2G={0}".format(x2G))
print("x2B={0}".format(x2B))
# x2, p, dof, expected = sp.stats.chi2_contingency(x)

# print("カイ二乗値は %(x2)s" %locals() )
# print("確率は %(p)s" %locals() )
# print("自由度は %(dof)s" %locals() )
# print( expected )

# if p < 0.05:
#     print("有意な差があります")
# else:
#     print("有意な差がありません")

# x2, p, dof, expected = sp.stats.chi2_contingency(imgRCount)

# print("カイ二乗値は %(x2)s" %locals() )
# print("確率は %(p)s" %locals() )
# print("自由度は %(dof)s" %locals() )
# print( expected )

# if p < 0.05:
#     print("有意な差があります")
# else:
#     print("有意な差がありません")

# x2, p, dof, expected = sp.stats.chi2_contingency(imgGCount)

# print("カイ二乗値は %(x2)s" %locals() )
# print("確率は %(p)s" %locals() )
# print("自由度は %(dof)s" %locals() )
# print( expected )

# if p < 0.05:
#     print("有意な差があります")
# else:
#     print("有意な差がありません")

# x2, p, dof, expected = sp.stats.chi2_contingency(imgBCount)

# print("カイ二乗値は %(x2)s" %locals() )
# print("確率は %(p)s" %locals() )
# print("自由度は %(dof)s" %locals() )
# print( expected )

# if p < 0.05:
#     print("有意な差があります")
# else:
#     print("有意な差がありません")
