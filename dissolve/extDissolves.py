import ditictFunc
import glob
import numpy as np


path = "../GoogleNet-Inception-tf/datasets/frames/*"
files = np.array(sorted(glob.glob(path)))

for pathName in files:
    print(pathName+"/*")
    ditictFunc.extDissloveFlame(pathName+"/*")
