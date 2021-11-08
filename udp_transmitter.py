import cv2
import socket
import math
import pickle
import sys
import imutils
import datetime

max_length = 65000
host = '172.17.155.126' #'10.24.128.2' #sys.argv[1] #Here you write the IP address of the destination
port = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

while ret:
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=512)
    #frame = cv2.resize(frame, (512, 512))

    # grab the current timestamp and draw it on the frame
    timestamp = datetime.datetime.now()
    cv2.putText(frame, 'transmitter timer: '+timestamp.strftime(
        "%I:%M:%S.%f"), (10, frame.shape[0] - 10),    #"%A %d %B %Y %I:%M:%S%f"
    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    cv2.imshow("TRANSMITTING VIDEO",frame)
    if cv2.waitKey(1) == '13':
        break    

    # compress frame
    retval, buffer = cv2.imencode(".jpg", frame)

    if retval:
        # convert to byte array
        buffer = buffer.tobytes()
        # get size of the frame
        buffer_size = len(buffer)

        num_of_packs = 1
        if buffer_size > max_length:
            num_of_packs = math.ceil(buffer_size/max_length)

        frame_info = {"packs":num_of_packs}

        # send the number of packs to be expected
        print("Number of packs:", num_of_packs)
        sock.sendto(pickle.dumps(frame_info), (host, port))
        
        left = 0
        right = max_length

        for i in range(num_of_packs):
            print("left:", left)
            print("right:", right)

            # truncate data to send
            data = buffer[left:right]
            left = right
            right += max_length

            # send the frames accordingly
            sock.sendto(data, (host, port))
    
    # ret, frame = cap.read()
    # cv2.imshow("TRANSMITTING VIDEO",frame)
    # if cv2.waitKey(1) == '13':
    #     break

print("done")