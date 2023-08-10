import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import glob
import pandas as pd


# ①ディゾルブ検出の処理
# ②rgbによるシーン検出の処理

def extDissloveFlame(path):
    image_arrays= np.empty((0))
    image_arrays2= np.empty((0))
    files = sorted(glob.glob(path))

    count = 0

    # ② -------------------
    # 256を分割する変数
    class_x = 32
    # class_x = 64
    # 色ごとに256/classX分割する関数
    def classRGB(x):
        return np.floor(x/class_x)

    for file in files:
        # ① ---------------
        #画像open(グレースケール)
        img = Image.open(file)
        imgG = img.convert('L')
        width, height = img.size
        #画像をリサイズ(縦横1/16)
        img_resized = imgG.resize((width//16, height//16))
        #画像データ取得(グレースケール)
        imgData2 = img_resized.getdata()
        width2, height2 = img_resized.size
        imgData2 = np.array(imgData2)
        image_arrays2 = np.append(image_arrays2, imgData2)
        # ② -------------------
        # rgbの処理
        img = img.resize((width//4, height//4))
        imgData = np.array(img)
        image_arrays = np.append(image_arrays, imgData)
        count += 1

    # ① -----------------------
    # 3次元配列に変換
    image_arrays2 = image_arrays2.reshape(count, height2, width2)

    # ② ------------------------
    # rgb用の画像サイズ取得
    width, height = img.size
    # 4次元配列に変換
    image_arrays = image_arrays.reshape(count, height, width, 3)


    # ①ディゾルブ検出の処理
    # 各フレームの画素の差分の配列
    d_image_arrays= np.empty((0))
    # 各フレームの画素の差分の配列
    r_imgs = np.empty((0))

    # ②rgbによるシーン検出の処理
    # 画像フレームを縦横4分割
    block_w = int(width/4)
    block_h = int(height/4)
    # rgbの色を分割する変数
    classX = int(256/class_x)
    # 各フレームの評価値リスト
    value_list = np.empty(0)

    for ix in range(1,len(image_arrays2)):
        # ① -----------------------------
        # 現在フレームと前フレームの差分
        d_img = image_arrays2[ix]-image_arrays2[ix-1]
        d_image_arrays = np.append(d_image_arrays, d_img)
        d_image_arrays = d_image_arrays.reshape(ix, height2, width2)

        #現フレームと前フレームの差分の比が正になる画素の全体に占める割合
        if ix>1:
            r_img = d_img/d_image_arrays[ix-2]
            r_img= np.floor(r_img * 10) / 10
            r_img[np.isnan(r_img)] = 0
            r_img[np.isinf(r_img)] = 1
            count = np.count_nonzero(0<r_img)/(width2*height2)
            r_imgs = np.append(r_imgs, count)

        # ② -------------------------------
        img1 = image_arrays[ix-1]
        img2 = image_arrays[ix]
        # 各フレームの評価値リスト
        x2_list = np.empty(0)

        # ブロックごとにrgbの分布を調べる
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

        x2_list = np.sort(x2_list)
        value = np.sum(x2_list[:10])
        value_list = np.append(value_list, value)

    # ①の処理
    # pandasに変換(データの平滑化を行うため)
    df = pd.Series(r_imgs)
    md = 3
    # 平均値フィルタ
    df = df.rolling(md, center=True).mean()
    # リストに戻す
    r_imgs = df.values.tolist()
    # フィルタによって生じたNaNを除去
    r_imgs=r_imgs[int((md-1)/2):int(-(md-1)/2)]


    # ②の処理
    # pandasに変換(データの平滑化を行うため)
    df2 = pd.Series(value_list)
    # メディアンフィルタ
    df2 = df2.rolling(3, center=True).mean()
    # リストに変換
    value_list = df2.values.tolist()
    value_list=value_list[int((md-1)/2):int(-(md-1)/2)]
    value_list=value_list[:-1]

    y_max = 0.1
    if np.nanmax(r_imgs)<=0.5:
        y_max = 0.5
    else:
        y_max = np.nanmax(r_imgs)+0.1
    y_max2 = 0.1
    if np.nanmax(value_list)<=5000:
        y_max2 = 5000
    else:
        y_max2 = np.nanmax(value_list)+2000

    # ②の処理
    # 画素の閾値
    value_list = np.array(value_list)
    value_list[value_list<850] = 0.01
    value_list[value_list>850] = 1

    r_imgs = r_imgs*value_list

    r_imgs=np.insert(r_imgs,0,r_imgs[0])
    r_imgs=np.append(r_imgs,r_imgs[-1])

    ext_file = np.empty(0)
    for i in range(len(r_imgs)):
        # 閾値以上のフレーム抽出()
        if r_imgs[i]>0.5:
            if i!=0:
                ext_file=np.append(ext_file,files[i-1])
            ext_file=np.append(ext_file,files[i])
            ext_file=np.append(ext_file,files[i+1])

    ext_file = np.unique(ext_file)

    f = open('dissolve/extract.txt', 'a')
    f.write(path+"\n")
    for ext_name in ext_file:
        f.write(ext_name+"\n")
    f.write("\n")
    f.close()



