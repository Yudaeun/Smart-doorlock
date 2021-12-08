import socket
import time
import adafruit_dht
import threading
import os
from board import *
SENSOR_PIN = D4

GPIO.setmode(GPIO.BCM)

dht11 = adafruit_dht.DHT11(SENSOR_PIN, use_pulseio=False)
temperature=0
humidity=0

def get_dht():
	global temperature
	global humidity

	while True:
		try:
			temperature = dht11.temperature
			humidity = dht11.humidity
			print(f"Humidity= {humidity:.2f}")
			print(f"Temperature= {temperature:.2f}°C")
		except RuntimeError:
            			print('Failed')
		time.sleep()


def server():
    HOST = "192.168.137.155"
    PORT = 8091
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')
    s.bind((HOST, PORT))
    print ('Socket bind complete')
    s.listen(1)
    print ('Socket now listening')
    



    while True:
    
     #접속 승인
        conn, addr = s.accept()
        print("Connected by ", addr)

    #데이터 수신
        data = conn.recv(1024)
        data = data.decode("utf8").strip()
        if not data: break
        print("Received: " + data)

    #수신한 데이터로 파이를 컨트롤 
        if input_string == "send":  # 휴대폰에서 send 라는 값이 올경우 ...라는 값을 돌려준다.
            input_string = "..."

        else:
            input_string = input_string + " 없는 명령어 입니다."
        print("파이 동작 :" + res)
        conn.sendall(res.encode("utf-8"))

    #연결 닫기
    s.close()



dht_thread=threading.Thread(target=get_dht)
server_thread=threading.Thread(target=server)
dht_thread.daemon=True
server_thread.daemon=True
server_thread.start()
dht_thread.start()
server_thread.join()
dht_thread.join()
print("end...")