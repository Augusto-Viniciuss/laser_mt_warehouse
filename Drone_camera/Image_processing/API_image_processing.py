import socket
import base64
import io
import PIL.Image as Image
import cv2


def barCodeProcessor(path):
        barCodeDetector = cv2.barcode_BarcodeDetector()
        image = cv2.imread(path)
        ok, decodedInfo, _, _ = barCodeDetector.detectAndDecode(image)
        
        print(f"Read Status: {ok}")
        if ok:
            print(f"Decoded Information: {decodedInfo}")


HOST = "192.168.1.46"  
PORT = 4000

imageNumber = 0
path = "/home/Augusto_V/Documents/Mambo-Turtle-Warehouse/Drone_camera/Image_processing/Images_processeds/Bc_"
imageBytes = bytes()
received = False

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
    socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_server.bind((HOST, PORT))
    socket_server.listen()
    conn, addr = socket_server.accept()
    
    while conn:
        print(f"Connected by {addr}")

        while conn:
            data = conn.recv(2048)
            
            if data.find(b"[") != -1 and not received:
                imageBytes += data[data.find(b"[") + 1:]
                received = True
                     
            if data.find(b"]") != -1:
                imageBytes += data[:data.find(b"]")]
                imageBytes = base64.b64decode(imageBytes + b'===', b'+/')
                
                image = Image.open(io.BytesIO(imageBytes))
                image.save(path + str(imageNumber) + ".jpg", "JPEG")
                barCodeProcessor(path + str(imageNumber) + ".jpg")
                
                imageNumber += 1
                received = False
                
                if data.find(b"[") != -1:
                    imageBytes = data[data.find(b"[") + 1:]
                    received = True
                else:
                    imageBytes = b''
                    received = False
            elif not data.find(b"[") != -1 and received:
                imageBytes += data