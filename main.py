import cv2
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller,Key

from cvzone.HandTrackingModule import HandDetector



cap = cv2.VideoCapture(0)
cap.set(3,1860)
cap.set(4,1080)

cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

detector = HandDetector(detectionCon=0.8,maxHands=2)
keys = [
    ['1','2','3','4','5','6','7','8','9','0'],
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L',';'],
    ['Z','X','C','V','B','N','M',',','.','/']
]

keyboard = Controller()
finalText = ''
delayCounter = 0 

def drawAll(img,buttonList):
    for button in buttonList:

        x,y = button.pos
        w,h = button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x + 20, y + 60),
                    cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img



def drawAll2(img,buttonList):
    imgNew = np.zeros_like(img,np.uint8)
    for button in buttonList:

        x,y = button.pos
        w,h = button.size
        cvzone.cornerRect(imgNew,(x,y,w,h),20,rt=0)
        cv2.rectangle(imgNew,(x,y),(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(imgNew,button.text,(x + 20, y + 60),
                    cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
        out = cv2.addWeighted(img,0.5,imgNew,0.5,0)
    

    
    return out


class Buttion():
    def __init__(self,pos,text,size=[75,75]):
        self.pos = pos
        self.text =text
        self.size = size
    
        
        
        





buttonList = []

# Number row
for x, key in enumerate(keys[0]):
    buttonList.append(Buttion([120 + x*85, 20], key))

# QWERTY row
for x, key in enumerate(keys[1]):
    buttonList.append(Buttion([185 + x*85, 120], key))

# ASDF row
for x, key in enumerate(keys[2]):
    buttonList.append(Buttion([225 + x*85, 220], key))

# ZXCV row
for x, key in enumerate(keys[3]):
    buttonList.append(Buttion([230  + x*85, 320], key))

# Backspace
buttonList.append(Buttion([990, 20], "Back", [190, 75]))

# Tab
buttonList.append(Buttion([20, 120], "Tab", [150, 75]))

# Caps Lock
buttonList.append(Buttion([20, 220], "Caps", [190, 75]))

# Enter
buttonList.append(Buttion([1075, 220], "Enter", [205, 75]))

# Shift
buttonList.append(Buttion([20, 320], "Shift", [200, 75]))

# Ctrl
buttonList.append(Buttion([20, 420], "Ctrl", [150, 75]))

# Alt
buttonList.append(Buttion([180, 420], "Alt", [120, 75]))

# Space
buttonList.append(Buttion([320, 420], "Space", [500, 75]))

# Right Alt
buttonList.append(Buttion([850, 420], "Alt", [120, 75]))

# Right Ctrl
buttonList.append(Buttion([980, 420], "Ctrl", [150, 75]))


while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands,img = detector.findHands(img)
    img = drawAll2(img,buttonList)
    

    

    






    if hands:
        for hand in hands:
            lmList = hand["lmList"]
            bbox = hand["bbox"]
            handType = hand["type"]
            for  button in buttonList:
                x,y = button.pos
                w,h = button.size 
                if x < lmList[8][0] <x+w and y<lmList[8][1] <y+h:
                    cv2.rectangle(img,button.pos,(x+w,y+h),(175,205,175),cv2.FILLED)
                    cv2.putText(img,button.text,(x + 20, y + 60),
                                cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    
                    l, _, _ = detector.findDistance(
                        lmList[8][:2],
                        lmList[12][:2],
                        img)
                    ## When Clicked
                    if l < 30 and delayCounter == 0:
                        if button.text == "Space":
                            keyboard.press(Key.space)
                            keyboard.release(Key.space)
                        elif button.text == "Back":
                            keyboard.press(Key.backspace)
                            keyboard.release(Key.backspace)
                        elif button.text == "Enter":
                            keyboard.press(Key.enter)
                            keyboard.release(Key.enter)
                        elif button.text == "Tab":
                            keyboard.press(Key.tab)
                            keyboard.release(Key.tab)
                        elif button.text == "Caps":
                            keyboard.press(Key.caps_lock)
                            keyboard.release(Key.caps_lock)
                        elif button.text == "Shift":
                            keyboard.press(Key.shift)
                            keyboard.release(Key.shift)
                        elif button.text == "Ctrl":
                            keyboard.press(Key.ctrl)
                            keyboard.release(Key.ctrl)
                        elif button.text == "Alt":
                            keyboard.press(Key.alt)
                            keyboard.release(Key.alt)
                        else:
                            keyboard.press(button.text.lower())   # or button.text
                            keyboard.release(button.text.lower())
                        cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                        cv2.putText(img,button.text,(x + 20, y + 60),
                                    cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    
                        if button.text == "Space":
                            finalText += " "

                        elif button.text == "Back":
                            finalText = finalText[:-1]

                        elif button.text == "Enter":
                            finalText += "\n"
                                 # or print(finalText)

                        else:
                            finalText += button.text
                        delayCounter = 1 
                            
                        
            


                    


        



    # Reset delay counter
    if delayCounter != 0:
        delayCounter += 1

        if delayCounter > 10:
            delayCounter = 0
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    



