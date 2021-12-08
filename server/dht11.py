# server2.py : 계속 보낼값 입력해 보낼 수 있음.
import socket
import time
import adafruit_dht
import threading
import os
from board import *
# GPIO4
SENSOR_PIN = D4

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
		time.sleep(0.5)

def server():
	global temperature
	connection=False
	host = '192.168.137.155' # Symbolic name meaning all available interfaces
	port = 8091 # Arbitrary non-privileged port
 

	server_sock = socket.socket(socket.AF_INET)
	server_sock.bind((host, port))
	server_sock.listen(1)

	print("waiting...")
	client_sock, addr = server_sock.accept()

	print('Connected by', addr)
	

	if(connection==False):
		client_sock, client_info=server_sock.accept()
		connection=True
		print("connected")
	

	data = client_sock.recv(1024)
	print(data.decode("utf-8"), len(data))


	while(True):
		data2 = int(temperature)
		#print(data2.encode())
		#client_sock.send(data)
		#client_sock.send(data2.to_bytes(4, byteorder='little'))
		i = 2
		if input_string == "send":  # 휴대폰에서 send 라는 값이 올경우 ...라는 값을 돌려준다.
			input_string = "..."
    # 값하나 보냄(사용자가 입력한 숫자)
		client_sock.send(str(data2).encode("utf-8"))
		client_info.sendall(data2.encode("utf-8"))

	client_sock.close()
	server_sock.close()


dht_thread=threading.Thread(target=get_dht)
server_thread=threading.Thread(target=server)
dht_thread.daemon=True
server_thread.daemon=True
server_thread.start()
dht_thread.start()
server_thread.join()
dht_thread.join()
print("end...")
    	