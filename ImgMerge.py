# -*- coding: euc-kr -*-
import glob
from PIL import Image  

def calc_size(files) :
    size_x = 0
    sizes = []
    for file in files:
        image = Image.open(file)
        size_x = image.size[0]
        sizes.append(image.size[1])
    size_y = sum(sizes)
    return size_x, size_y
def img_merge(files, x_size, y_size) :
    new_img = Image.new("RGB",(x_size,y_size),(256,256,256))
    now_y = 0
    for file in files :
        img = Image.open(file)
        area = (0,now_y,x_size,now_y+img.size[1])
        now_y = now_y + img.size[1]
        new_img.paste(img,area)
    return new_img

def Merge(tar_dir) :
    files = glob.glob(tar_dir+"\\*.*")
    size_x, size_y = calc_size(files)
    img = img_merge(files,size_x,size_y)
    num = '_E' + tar_dir[tar_dir.rfind('\\')+1:].zfill(3)
    title = tar_dir[:tar_dir.rfind('\\')]
    title = '\\'+title[title.rfind('\\')+1:]
    tar_dir = tar_dir[:tar_dir.rfind('\\')] + title + num + '.jpg' 
    img.save(tar_dir,'JPEG')