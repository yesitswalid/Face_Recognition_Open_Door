#importing GPIO

#This is for raspberry pi
import RPi.GPIO as GPIO

import servo

def open():
    servo.SetAngle(90)
    print("la porte est ouverte !")


def close():
    servo.SetAngle(0)
    print("la porte est fermé !")