import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import sys
import qrcode

def im (k):
    width, height = 666, 333 #Ширина и высота картинки
    img = Image.new('RGBA', (width, height), 'white')    
    idraw = ImageDraw.Draw(img)
    text = str(k)
    font = ImageFont.truetype("arialbd.ttf", size=260)
    idraw.text((width/2, 96), text, 'black', anchor="mm", font=font)
    im = img.rotate(270, expand=True)
    return im
def img_qr (G):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
        )

    qr.add_data(G)
    qr.make(fit=True)

    imgqr = qr.make_image(fill_color="black", back_color="white")
    return imgqr

data = pd.read_excel ('Таблица для qr.xlsx')
    
for index, row in data.iterrows():
    a = row['ID']
    b = row['Ссылка']    
    
    #Создание картинки с номером ID
    imtext = im (a)       
    
    #Узнаём размер картинки с ID
    shir1, visot1 = imtext.size
    
    #Создание QR-кода с уменьшиными рамками
    imgqr = img_qr (b)
    
    
    # Изменяем масштаб QR-кода пропорционально по высоте
    qr_shir, qr_visot = imgqr.size
    visot2 = visot1
    shir2 = int((qr_shir / qr_visot) * visot2)
    imgqr = imgqr.resize((shir2, visot2))
   
    #Создаём картинку с размерами 2 созданных, где их объединим
    new_visot = max (visot1, visot2)
    new_shir = shir1 + shir2
    new_img = Image.new ('RGB', (new_shir, new_visot))
    
    #Копируем 1 изображение в новую картинку
    new_img.paste (imtext, (0,0))
    
    # Копируем вторую картинку в новое изображение, начиная с позиции после первой картинки
    new_img.paste (imgqr, (shir1,0))
    
    #Сохраняем полученный результат
    new_img.save (f'{a}.png')