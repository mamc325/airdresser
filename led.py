import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #BCM 모드로 작동
GPIO.setwarnings(False) #경고글이 출력되지 않게 설정
# LED를 다루기 위한 전역 변수 선언 및 초기화
led = 6 # GPIO6
green = 13 # GPIO13
red = 19 # GPIO21
GPIO.setup(led, GPIO.OUT) # GPIO6 핀을 출력으로 지정
GPIO.setup(green, GPIO.OUT) # GPIO13 핀을 출력으로 지정

GPIO.setup(red, GPIO.OUT) # GPIO19 핀을 출력으로 지정

# LED를 켜고 끄는 함수
def controlLED(on_off): # led 번호의 핀에 on_off(0/1) 값 출력하는 함수	
	GPIO.output(led, on_off)
def control_green(bright):
    GPIO.output(green, bright)
def control_red(danger):
    GPIO.output(red, danger)

