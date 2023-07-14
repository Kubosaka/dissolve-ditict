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
# class_x = 32
class_x = 64
# 色ごとに4分割する関数
def classRGB(x):
    return np.floor(x/class_x)

image_arrays= np.empty((0))
files = sorted(glob.glob("./frames2/*"))

count = 0
for file in files:
    #画像open(グレースケール)
    img = Image.open(file)
    width, height = img.size
    #画像データ取得
    imgData = np.array(img)
    image_arrays = np.append(image_arrays, imgData)
    count += 1


# 4次元配列に変換
image_arrays = image_arrays.reshape(count, height, width, 3)

# 画像フレームを縦横4分割
block_w = int(width/4)
block_h = int(height/4)
print(width)
print(height)
print()

# rgbの色を分割する変数
classX = int(256/class_x)

for ih in range(block_h,height+1,block_h):
    for iw in range(block_w, width+1,block_w):
        print("hは{0}:{1},wは{2}:{3}".format(ih-block_h,ih,iw-block_w,iw))
        blockImage=image_arrays[0, ih-block_h:ih, iw-block_w:iw]
        blockImage2=image_arrays[1, ih-block_h:ih, iw-block_w:iw]
        r = classRGB(blockImage[:,:,0])
        r2 = classRGB(blockImage2[:,:,0])
        g = classRGB(blockImage[:,:,1])
        g2 = classRGB(blockImage2[:,:,1])
        b = classRGB(blockImage[:,:,2])
        b2 = classRGB(blockImage2[:,:,2])
        # 色の要素を保存するリスト

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
        
        # # 1枚目と2枚目のフレームの差分の2次元リストに
        # imgRCount= np.append(imgRCount, imgRCount2).reshape(2, classX)
        # imgGCount= np.append(imgGCount, imgGCount2).reshape(2, classX)
        # imgBCount= np.append(imgBCount, imgBCount2).reshape(2, classX)
        print(imgRCount)
        print(imgGCount)
        print(imgBCount)
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

            kaiR = (oiR-eiR)**2/eiR
            x2R += kaiR


            kaiG = (oiG-eiG)**2/eiG
            x2G += kaiG

            kaiB = (oiB-eiB)**2/eiB
            x2B += kaiB
        
        print("x2R={0}".format(x2R))
        print("x2G={0}".format(x2G))
        print("x2B={0}".format(x2B))
        print()



