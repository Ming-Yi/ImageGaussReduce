# -*- coding: utf-8 -*-
from PIL import Image
from collections import defaultdict

'''
檢查所有圖片大小是否一致
'''
def CheckImageSize(ImagesSizeList):
    count = defaultdict(int)
    for ImagesSize in ImagesSizeList:
        count[ImagesSize]+=1
    if len(count) == 1:
        return True
    else:
        return False

'''
載入影像
'''
def ReadImageFile(ImagePathList):
    # 將每一章影像的pixel載入的list
    Images = list() 
    # 取得每張圖片的大小
    ImagesSizeList = list() 

    for ImagePath in ImagePathList:
        imtemp = Image.open(ImagePath)
        Images.append(imtemp.load())
        ImagesSizeList.append(imtemp.size)
    return Images,ImagesSizeList

'''
降低高斯雜訊
'''
def ReduceNoise(Images, ImagesSizeList):
    if CheckImageSize(ImagesSizeList):
        OutputImage = Image.new("RGB", ImagesSizeList[0])
        ix,iy = ImagesSizeList[0]
        for x in xrange(ix):
            for y in xrange(iy):
                R,G,B = 0,0,0 
                for im in Images:
                    r,g,b = im[x,y]
                    R+=r
                    G+=g
                    B+=b
                R = int(R/len(Images))
                G = int(G/len(Images))
                B = int(B/len(Images))
                OutputImage.putpixel((x,y),(R,G,B))
        OutputImage.save("output.jpg")
    else :
        print "輸入圖片大小不一致"

def main():
    ImagePathList = ["_MG_3744.JPG","_MG_3745.JPG","_MG_3746.JPG"]
    Images, ImagesSizeList = ReadImageFile(ImagePathList)
    ReduceNoise(Images, ImagesSizeList)

if __name__ == '__main__':
    main()


    