#publisher
import ultrasonic
import io
import time
from PIL import Image
import paho.mqtt.client as mqtt
import camera
import led
import spearker 
import temp
import lumi

isStart = False
bzStart = False

def on_connect(client, userdata, msg, rc):
    client.subscribe("camera")
    client.subscribe("led", qos=0)  # "led" 토픽으로 구독 신청
    client.subscribe("buzzer")	#"buzzer" 토픽으로 구독 신청
def on_message(client, userdata, msg):
    global isStart

    # LED 제어
    if msg.topic == "led":
        on_off = int(msg.payload)  # on_off는 0 또는 1의 정수
        led.controlLED(on_off)  # LED를 켜거나 끔

    # 카메라 제어
    elif msg.topic == "camera":
        if msg.payload.decode('utf-8') == 'start':
            isStart = True
            print("Start Camera")
        else:
            isStart = False
            print("Stop Camera")
    #부저 제어
    elif msg.topic == "buzzer":
         start_stop = int(msg.payload)  #start_stop는 0또는 1의 정수
         spearker.speaker(start_stop)
            
broker_ip = "localhost"

client = mqtt.Client()
client.connect(broker_ip, 1883)  # 1883 포트로 mosquitto에 접속
client.on_connect = on_connect
client.on_message = on_message

client.loop_start()  # 메시지 루프를 실행하는 스레드 생성

ultrasonic.init()  # 초음파 센서 초기화
ultrasonic.setTrigEcho(20, 16)  # 초음파 센서의 Trig와 Echo 핀 설정
camera.init()  # 카메라 초기화
stream = io.BytesIO()

last_save_time = time.time()
while True:
	if isStart:
		distance = ultrasonic.measureDistance()  # 초음파 센서로 거리 측정
		temperature = temp.getTemperature(temp.sensor)# 센서로부터 온도 값 수신 함수
		client.publish("temperature", temperature, qos=0) # “templates” 토픽으로 거리 전송
		humidity = temp.getHumidity(temp.sensor)# 센서로부터 습도 값 수신 함수
		luminance = lumi.getLuminance()
		if luminance <= 50: 
			bright = 1
			led.control_green(bright)
		elif luminance >50:
			bright = 0 
			led.control_green(bright)
		if temperature >= 27:
			danger = 1
			led.control_red(danger)
			spearker.speaker(danger)
		elif temperature <27:
			danger = 0	
			led.control_red(danger)
		client.publish("humidity", humidity, qos=0) # "humidity" 토픽으로 습도 전송
		frame = camera.take_picture()
		stream.seek(0)  # stream 파일의 커서를 맨 앞으로 이동한다
		image = Image.fromarray(frame)  # numpy array 데이터를 PILLOW의 image 데이터 포맷으로 변환
		image.save(stream, format='JPEG')  # 이미지 변환후 JPEG 형식으로 이미지를 저장

		client.publish("image", stream.getvalue(), qos=0)  # image토픽으로 이미지 데이터 전송
		stream.truncate(0)  # stream 파일에 있는 모든 내용을 지우고 커서를 처음으로 이동

		current_time = time.time()
		if distance <= 20 and current_time - last_save_time >= 3:
			filename = time.strftime("%Y년%m월%d일%H시%M분%S초") + ".jpg"
			image.save(filename, format='JPEG')

			print(f"출입 감지: {filename}")
			last_save_time = current_time
	else:
		time.sleep(1)


camera.release()  # 카메라 사용 끝내기
client.loop_stop()  # 메시지 루프를 실행하는 스레드 종료
client.disconnect()
