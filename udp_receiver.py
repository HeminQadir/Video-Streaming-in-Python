import cv2
import socket
import pickle
import numpy as np
import datetime

host_name  = socket.gethostname()
host_ip = '192.168.8.102' #socket.gethostbyname(host_name)   # This is the destination, so it has to pick up its own IP. if not change it manually
print('HOST IP:',host_ip)
port = 8080
max_length = 65540
# Socket Create

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((host_ip, port))

frame_info = None
buffer = None
frame = None

print("-> WAITING FOR CONNECTION ..... ")
connection = True

while True:
    data, address = sock.recvfrom(max_length)
    if connection:
        print('GOT CONNECTION FROM:', address)
        connection = False  
    if len(data) < 100:
        frame_info = pickle.loads(data)

        if frame_info:
            nums_of_packs = frame_info["packs"]

            for i in range(nums_of_packs):
                data, address = sock.recvfrom(max_length)

                if i == 0:
                    buffer = data
                else:
                    buffer += data

            frame = np.frombuffer(buffer, dtype=np.uint8)
            frame = frame.reshape(frame.shape[0], 1)

            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            #frame = cv2.flip(frame, 1)
            
            if frame is not None and type(frame) == np.ndarray:

                timestamp = datetime.datetime.now()
                cv2.putText(frame, 'RX timer: '+timestamp.strftime("%I:%M:%S.%f"), (10, frame.shape[0] - 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv2.imshow("RECEIVING VIDEO", frame)
                if cv2.waitKey(1) == 27:
                    break
                
print("goodbye")