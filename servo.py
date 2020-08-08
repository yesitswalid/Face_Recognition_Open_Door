import RPi.GPIO as GPIO
from time import sleep

#This is the Servo PIN.
SERVO_PIN = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SERVO_PIN, GPIO.OUT)


#Define the max frequence of the PIN 50 Hz
pwm=GPIO.PWM(SERVO_PIN, 50)
pwm.start(0) #Starting frequence to 0


#This is duty calculation between the cycle and angle.
#Source from: https://www.learnrobotics.org/blog/raspberry-pi-servo-motor/
def setAngle(angle):

    duty = angle / 18 + 3
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(duty)


pwm.stop()
GPIO.cleanup()