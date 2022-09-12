import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np


cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8) # Criação do detector e configuração da sua precisão
colorR = (209,149,0)

cx, cy, w, h = 50, 50, 100, 100

class DragRect():
    def __init__(self, posCenter, size=[100,100]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size
        if cx - w // 2 < cursor[0] < cx + w // 2 and \
                cy - h // 2 < cursor[1] < cy + h // 2:  # Se os pontos do Traking estiverem dentro das coodenadas que limitam a existência do quadrado, a cor do objeto mudará para verde
            self.posCenter = cursor


rectList = []
for x in range(3):
    rectList.append(DragRect([x*250+150, 150]))
rect = DragRect([100, 100])

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # Inverter a imagem (Captura da tela) no eixo x
    img = detector.findHands(img)
    lmList, _ = detector.findPosition(img)

    if lmList: # Encontrar a posição das falanges e Identificar a interação com os objetos
        l, _, _ = detector.findDistance(8, 12, img)
        print(l)
        if l < 30:
            cursor = lmList[8] # Index da falange
            # Chamar os updates aqui
            for rect in rectList:
                rect.update(cursor)

    ##-- Criação de blocos Sólidos --#
    #for rect in rectList:
    #    cx, cy = rect.posCenter
    #    w, h = rect.size
    #    cv2.rectangle(img, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED) # Criação do quadrado que aparecerá na tela
    #    cvzone.cornerRect(img, (cx-w//2, cy-h//2, w, h), 10, rt=0)

    ##-- Criação de blocos Transparentes --#
    imgNew = np.zeros_like(img, np.uint8)
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv2.rectangle(imgNew, (cx-w//2, cy-h//2), (cx+w//2, cy+h//2), colorR, cv2.FILLED) # Criação do quadrado que aparecerá na tela
        cvzone.cornerRect(imgNew, (cx-w//2, cy-h//2, w, h), 10, rt=0)

        out = img.copy()
        alpha = 0.1
        mask = imgNew.astype(bool)
        out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]


    cv2.imshow("Image", out)
    cv2.waitKey(1)


