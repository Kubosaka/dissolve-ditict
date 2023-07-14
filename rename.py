import os
from glob import glob
import datetime

current_dir = os.getcwd()

current_dir+="/frames"

path_list = glob(os.path.join(current_dir, "*.jpg"))
path_list = sorted(path_list)

for i,path in enumerate(path_list):
    dirname, file_and_ext = os.path.split(path)
    file, ext = os.path.splitext(file_and_ext)
    if i+1<10:
        number="000"
    elif i+1<100:
        number="00"
    elif i+1<1000:
        number="0"
    else:
        number=""
    number+=str(i+1)
    new_file_name = number+ext
    os.rename(path, os.path.join(dirname, new_file_name))
