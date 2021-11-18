import time
import adafruit_dht
import threading
import os
import glob
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
	host='192.168.0.7'
	port=22
	server_sock = socket.socket(socket.AF_INET)
	server_sock.bind((host, port))
	server_sock.listen(1)
	print("waiting..")
	out_data = int(10)

	while True: 
		client_sock, addr = server_sock.accept()
		if client_sock: 
			print('Connected by...', addr) 
			in_data = client_sock.recv(1024) 
			print('receive data :', in_data.decode("utf-8"), len(in_data)) 
			while in_data :
				client_sock.send(str(out_data).encode("utf-8")) 
				print('send temperature :', temperature)
				time.sleep(2)

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
    	