# -*- coding: utf-8 -*-

import cv2
import os
import math
from PIL import Image
from PIL import GifImagePlugin
GIFNAME = "tenor.gif"

imageObject = Image.open(GIFNAME)
print(imageObject.is_animated)

print(imageObject.n_frames)
Frame=imageObject.n_frames
#配列設定
#Frame = 30 #フレーム数
NUMPIXELS = 36 #LEDの数
Div = 120 #１周の分割数


Bright = 30 #輝度
Led0Bright = 3 #中心LEDの輝度 [%]


#ファイル作成
file = open('graphics.h', 'w')
file.write('#define Frame ' + str(Frame) + '\n')
file.write('#define NUMPIXELS ' + str(NUMPIXELS) + '\n')
file.write('#define Div ' + str(Div) + '\n' + '\n')
#file.write('#define Frame ' + str(Frame) + '\n' + '\n')


file.write('const uint32_t pic [Frame][Div][NUMPIXELS] = {' + '\n')

# Gifファイルを読み込む
# 参考 https://www.tech-tech.xyz/gif-divide.html
gif_file_name = GIFNAME
gif = cv2.VideoCapture(gif_file_name)


#画像変換関数
def polarConv(pic, i):
    imgOrgin = cv2.imread(pic) #画像データ読み込み
    
    h, w, _ = imgOrgin.shape #画像サイズ取得

    #画像縮小
    imgRedu = cv2.resize(imgOrgin,(math.floor((NUMPIXELS * 2 -1)/h *w), NUMPIXELS * 2 -1))
    #cv2.imwrite(str(i) + '-resize.jpg',imgRedu)

    #縮小画像中心座標
    h2, w2, _ = imgRedu.shape
    wC = math.floor(w2 / 2)
    hC = math.floor(h2 / 2)

    #極座標変換画像準備
    imgPolar = Image.new('RGB', (NUMPIXELS, Div))


    #極座標変換
    file.write('\t{\n')
    for j in range(0, Div):
        file.write('\t\t{')
        for i in range(0, hC+1):
            #座標色取得
            #参考：http://peaceandhilightandpython.hatenablog.com/entry/2016/01/03/151320
            rP = int(imgRedu[hC + math.ceil(i * math.cos(2*math.pi/Div*j)),
                         wC - math.ceil(i * math.sin(2*math.pi/Div*j)), 2]
                     * ((100 - Led0Bright) / NUMPIXELS * i + Led0Bright) / 100 * Bright /100)
            gP = int(imgRedu[hC + math.ceil(i * math.cos(2*math.pi/Div*j)),
                         wC - math.ceil(i * math.sin(2*math.pi/Div*j)), 1]
                     * ((100 - Led0Bright) / NUMPIXELS * i + Led0Bright) / 100 * Bright /100)
            bP = int(imgRedu[hC + math.ceil(i * math.cos(2*math.pi/Div*j)),
                         wC - math.ceil(i * math.sin(2*math.pi/Div*j)), 0]
                     * ((100 - Led0Bright) / NUMPIXELS * i + Led0Bright) / 100 * Bright /100)
            
            file.write('0x%02X%02X%02X' % (rP,gP,bP))
            
            if i == hC:
                file.write('},\n')
            else:
                file.write(', ')
                
            imgPolar.putpixel((i,j), (rP, gP, bP))
    file.write('\t},\n\n')



# スクリーンキャプチャを保存するディレクトリを生成
dir_name = "screen_caps"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)


for i in range(Frame):
    is_success, frame = gif.read()

    # 画像ファイルに書き出す
    img_name = str(i) + ".jpg"
    img_path = os.path.join(dir_name, img_name)
    cv2.imwrite(img_path, frame)

    #変換
    polarConv(img_path, i)
    


file.write('};' + '\n' + '\n')
file.close()
