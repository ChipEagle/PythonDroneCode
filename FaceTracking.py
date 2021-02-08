import cv2
import numpy as np 
from djitellopy import tello
from time import sleep

import os
import platform
import getpass

name = 'TELLO-62686A' # Change to Tello WiFi for your drone
key = ''

def findFace(img):
   faceCascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
   imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

   # Get the center of the detected face
   myFaceListC = []
   myFaceListArea = []

   for (x,y,w,h) in faces:
      cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
      cx = x + w // 2
      cy = y + h // 2
      area = w * h
      cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
      myFaceListC.append([cx, cy])
      myFaceListArea.append(area)
   if len(myFaceListArea) != 0:
      i = myFaceListArea.index(max(myFaceListArea))
      return img, [myFaceListC[i], myFaceListArea[i]]
   else:
      return img, [[0, 0], 0]

def trackFace(info, w, pid, pError):

   area = info[1]

   x, y = info[0]

   fb = 0

   error = x - w // 2
   speed = pid[0] * error + pid[1] * (error - pError)
   # Clip the speed between -100 and 100
   speed = int(np.clip(speed, -100, 100))

   
   # If the face is in the range, the drone should stay stationary
   if area > fbRange[0] and area < fbRange[1]:
      fb = 0
   # If the face is too close to the drone, move the drone backword 20 cm.
   elif area > fbRange[1]:
      fb = -20
   # If the face is too far from the drone and the face is detected, move the drone forward 20 cm.
   elif area < fbRange[0] and area != 0:
      fb = 20

   if x == 0:
      speed = 0
      error = 0

   # print(speed, fb)

   drone.send_rc_control(0, fb, 0, speed) 
   return error


def createNewConnection(name, SSID, key):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">n
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+key+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    if platform.system() == "Windows":
        command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
        with open(name+".xml", 'w') as file:
            file.write(config)
    elif platform.system() == "Linux":
        command = "nmcli dev wifi connect '"+SSID+"' password '"+key+"'"
    os.system(command)
    if platform.system() == "Windows":
        os.remove(name+".xml")
def connect(name, SSID):
    if platform.system() == "Windows":
        command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    elif platform.system() == "Linux":
        command = "nmcli con up "+SSID
    os.system(command)

   
# Connect to the Tello WiFi after the drone is powered up, this will connect on Windows and Linux platforms
createNewConnection(name, name, key)
connect(name, name)
print("If you aren't connected to this network, try connecting with the correct credentials")

# Wait 5 seconds for the Tello WiFi to connect
sleep(5)

drone = tello.Tello()
drone.connect()

lcBattery = drone.get_battery()
print(lcBattery)
liBattery = int(''.join(x for x in lcBattery if x.isdigit()))

print("The battery charge is: " + str(liBattery) + "%")

drone.streamon()

drone.takeoff()
drone.send_rc_control(0, 0, 25, 0) 
sleep(2.2)

# Size the image capture to width and hight
w, h = 360, 240

fbRange = [6200, 6800]
# Proportional, Integral, Derivator
pid = [0.4, 0.4, 0]
pError = 0


# Capture video from the web cam
# cap = cv2.VideoCapture(0)

while True:
   # _, img = cap.read()
   img = drone.get_frame_read().frame
   img = cv2.resize(img, (w, h))
   img, info = findFace(img)
   # pError = trackFace(drone, info, w, pid, pError)
   pError = trackFace(info, w, pid, pError)
   # print("Center", info[0], "Area", info[1])
   cv2.imshow("Output", img)
   if cv2.waitKey(1) & 0xFF == ord('q'):
      drone.land()
      break
