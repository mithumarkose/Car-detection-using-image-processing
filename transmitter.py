
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
radio.openWritingPipe(pipes[0])
radio.printDetails()

cam=PiCamera()
cam.resolution=(640,480)
cam.framerate=32
raw=PiRGBArray(cam, size=(640,480))
face_cascade=cv2.CascadeClassifier('/home/pi/cars.xml')

time.sleep(0.1)

message = list("ALERT: Vechile approaching")
while len(message) < 32:
    message.append(0)


for frame in cam.capture_continuous(raw, format="bgr" ,use_video_port=True):
    imag=frame.array
    img=cv2.cvtColor(imag,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(img,1.3,5)

    for (x,y,w,h) in faces:
        # To draw a rectangle in a face
        print"Hiii"
        cv2.rectangle(imag,(x,y),(x+w,y+h),(255,255,0),2) 
        roi_gray = img[y:y+h, x:x+w]
        roi_color = imag[y:y+h, x:x+w]
        start = time.time()
        radio.write(message)
        print("Sent the message: {}".format(message))
    
    cv2.imshow("Streaming",imag)
    key = cv2.waitKey(1) & 0xFF
    raw.truncate(0)
    
