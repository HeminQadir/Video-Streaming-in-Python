# This code is for the server 
# Lets import the libraries
import socket, cv2, pickle, struct, imutils, math

# Socket Create
max_length = 65000 
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = "172.17.155.126"   #socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 8080
socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
    client_socket,addr = server_socket.accept()
    print('GOT CONNECTION FROM:',addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        fr_no = 1
        while(vid.isOpened()):
            img,frame = vid.read()
            frame = imutils.resize(frame,width=320)
            #frame = imutils.resize(frame, (512, 512))

            # grab the current timestamp and draw it on the frame
            timestamp = datetime.datetime.now()
            cv2.putText(frame, 'transmitter timer: '+timestamp.strftime(
                "%I:%M:%S.%f"), (10, frame.shape[0] - 10),    #"%A %d %B %Y %I:%M:%S%f"
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            
            cv2.putText(frame, 'frame: '+str(fr_no), (10, frame.shape[0] - 40),    
            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            
            buffer_size = len(message) 
            num_of_packs = 1
            
            if buffer_size > max_length:
                num_of_packs = math.ceil(buffer_size/max_length)
                
            left = 0
            right = max_length 
            
            for i in range(num_of_packs):
                print("left:", left)
                print("right:", right)

                # truncate data to send
                data = message[left:right]
                left = right
                right += max_length
         
                client_socket.sendall(message)
            
            fr_no +=1
            
            cv2.imshow('TRANSMITTING VIDEO',frame)
            key = cv2.waitKey(1) & 0xFF
            if key ==ord('q'):
                client_socket.close()
                
