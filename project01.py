##--- Importação dos módulos ---##
import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

##-- Definição das variáveis e iniciação do dispositivo de captura de imagem --##
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8) # Criação do detector e configuração da sua precisão
colorR = (255, 0, 255)

cx, cy, w, h = 50, 50, 100, 100

##----------------------------------------##
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # Inverter a imagem (Captura da tela) no eixo x
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList: # Encontrar a posição das falanges e Identificar a interação com os objetos

        l, _, _ = detector.findDistance(8, 4, img)
        print(l)
        if l < 30:
            cursor = lmList[8]
            if cx-w//2 < cursor[0] < cx+w//2 and cy-h//2 < cursor[1] < cy+h//2: # Se os pontos do Traking estiverem dentro das coodenadas que limitam a existência do quadrado, a cor do objeto mudará para verde
                colorR = 0, 255, 0
                cx, cy = cursor

            else:
                colorR = (255, 0, 255)

    cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED) # Criação do quadrado que aparecerá na tela
    cv2.imshow("Image", img)
    cv2.waitKey(1)
