
import cv2
import math
from PIL import Image

NUMPIXELS = 36 #LEDの数
Div = 250 #１周の分割数

#画像データ読み込み
imgOrgin = cv2.imread('rock2.jpg')

#画像サイズ取得
#参考：https://note.nkmk.me/python-opencv-pillow-image-size/
h, w, _ = imgOrgin.shape
print('widthOrgin: ', w)
print('heightOrgin:', h)

#画像縮小
#参考：https://www.tech-tech.xyz/opecv_resize.html
imgRedu = cv2.resize(imgOrgin,(math.floor((NUMPIXELS * 2 -1)/h *w), NUMPIXELS * 2 -1))
cv2.imwrite('img-resize.jpg',imgRedu)

#縮小画像中心座標
h2, w2, _ = imgRedu.shape
print('widthRedu: ', w2)
print('heightRedu:', h2)
wC = math.floor(w2 / 2)
hC = math.floor(h2 / 2)
print('widthCenter: ', wC)
print('heightCenter:', hC)

#極座標変換画像準備
imgPolar = Image.new('RGB', (NUMPIXELS, Div))


#極座標変換
file = open('PolarConv.txt', 'w')

for j in range(0, Div):
    file.write('{')
    for i in range(0, hC+1):
        #座標色取得
        #参考：http://peaceandhilightandpython.hatenablog.com/entry/2016/01/03/151320
        rP = imgRedu[hC - math.ceil(i * math.cos(2*math.pi/Div*j)),
                     wC + math.ceil(i * math.sin(2*math.pi/Div*j)), 2]
        gP = imgRedu[hC - math.ceil(i * math.cos(2*math.pi/Div*j)),
                     wC + math.ceil(i * math.sin(2*math.pi/Div*j)), 1]
        bP = imgRedu[hC - math.ceil(i * math.cos(2*math.pi/Div*j)),
                     wC + math.ceil(i * math.sin(2*math.pi/Div*j)), 0]
        file.write('0x%02X%02X%02X' % (rP,gP,bP))
        
        if i == hC:
            file.write('},\n')
        else:
            file.write(', ')
            
        imgPolar.putpixel((i,j), (int(rP), int(gP), int(bP)))
    
file.close()

#変換画像保存
#参考：https://qiita.com/uosansatox/items/4fa34e1d8d95d8783536
imgPolar.save('PolarConv.jpg')
