import socket
import io
from PIL import Image
import numpy as np
import cv2
import time

def obtener_ip_conexion():
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    return ip_address

while True:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('0.0.0.0', 3500)
    print('Iniciando en {} puerto {}'.format(*server_address))
    server_socket.bind(server_address)

    ip_conexion = obtener_ip_conexion()
    print('Servidor corriendo en IP:', ip_conexion)

    server_socket.listen(1)

    print('Esperando conexión...')
    client_socket, client_address = server_socket.accept()
    print('Conexión establecida desde', client_address)

    image_data = b''
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        image_data += data

    client_socket.close()
    server_socket.close()

    with open("foto_recibida.png", "wb") as image_file: #guardar
        image_file.write(image_data)

    print('Imagen recibida y guardada correctamente')
    
    # imageP =cv2.imread("imgpc.jpg", cv2.IMREAD_UNCHANGED)
    # video=cv2.VideoCapture(1)
    # video=cv2.VideoCapture("172.16.212.130")
    # video=cv2.VideoCapture("videoEjemplo.mp4")
    video=cv2.VideoCapture("http://192.168.0.100:4747/video")
    imageT = cv2.imread("foto_recibida.png", cv2.IMREAD_UNCHANGED)

    if(video.isOpened):
        prev_time = time.time()
        while True:
            res,imageP= video.read()
            if not res:
                break
            imageP=cv2.flip(imageP, 1)

            resultado = np.zeros_like(imageP)
            
            if imageT.shape[2] == 4:
                imageT = imageT[:, :, :3]

            widthP,  heightP = imageP.shape[:2]
            widthT,  heightT = imageT.shape[:2]

            alter= cv2.resize(imageP,((widthT),heightT))
            print(alter.shape);
            columna =  0
            fila = 0
            end_row = min(fila + heightT, heightP)
            end_col = min(columna + widthT, widthP)
            mask = imageT[:, :, 2] != 0
            mask = imageT[:end_row - fila, :end_col - columna, 2] != 0
            # Filtro sepia
            sepia= alter.copy()
            mascara = np.array([[0.272, 0.534, 0.131],
                                    [0.349, 0.686, 0.168],
                                    [0.393, 0.769, 0.189]])

            sepia = cv2.transform(sepia, mascara)
            sepia = np.clip(sepia, 0, 255).astype(np.uint8)
            resultado=sepia
            resultado[fila:end_row, columna:end_col][mask] = imageT[:end_row - fila, :end_col - columna][mask]
            current_time = time.time()
            fps = 1 / (current_time - prev_time)
            prev_time = current_time
            cv2.putText(resultado, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow("Imagen Resultante", resultado)
            # Convertir imageP a BGRA
            if cv2.waitKey(1) & 0xFF == ord('q'): 
                video.release()
                cv2.destroyAllWindows()
                break
 


# import socket
# import io
# from PIL import Image
# import numpy as np
# import cv2
# import time
# from flask import Flask, request, jsonify, send_file, render_template
# import threading

# app = Flask(__name__)

# def obtener_ip_conexion():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 1))
#         ip_address = s.getsockname()[0]
#     except Exception:
#         ip_address = '127.0.0.1'
#     return ip_address

# def start_socket_server():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ('0.0.0.0', 3500)
#     server_socket.bind(server_address)
#     server_socket.listen(1)
#     print('Socket server running on {}:{}'.format(*server_address))

#     while True:
#         print('Waiting for a connection...')
#         client_socket, client_address = server_socket.accept()
#         print('Connection established from', client_address)

#         image_data = b''
#         while True:
#             data = client_socket.recv(1024)
#             if not data:
#                 break
#             image_data += data

#         client_socket.close()
        
#         with open("foto_recibida.png", "wb") as image_file:
#             image_file.write(image_data)

#         print('Image received and saved successfully')

#         process_image("foto_recibida.png")

# def process_image(image_path):
#     video = cv2.VideoCapture("http://192.168.0.100:4747/video")
#     imageT = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

#     if video.isOpened():
#         prev_time = time.time()
#         res, imageP = video.read()
#         if res:
#             imageP = cv2.flip(imageP, 1)
#             resultado = np.zeros_like(imageP)
            
#             if imageT.shape[2] == 4:
#                 imageT = imageT[:, :, :3]

#             widthP, heightP = imageP.shape[:2]
#             widthT, heightT = imageT.shape[:2]

#             alter = cv2.resize(imageP, (widthT, heightT))
#             columna = 0
#             fila = 0
#             end_row = min(fila + heightT, heightP)
#             end_col = min(columna + widthT, widthP)
#             mask = imageT[:, :, 2] != 0
#             mask = imageT[:end_row - fila, :end_col - columna, 2] != 0

#             sepia = alter.copy()
#             mascara = np.array([[0.272, 0.534, 0.131],
#                                 [0.349, 0.686, 0.168],
#                                 [0.393, 0.769, 0.189]])

#             sepia = cv2.transform(sepia, mascara)
#             sepia = np.clip(sepia, 0, 255).astype(np.uint8)
#             resultado = sepia
#             resultado[fila:end_row, columna:end_col][mask] = imageT[:end_row - fila, :end_col - columna][mask]
#             current_time = time.time()
#             fps = 1 / (current_time - prev_time)
#             prev_time = current_time
#             cv2.putText(resultado, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#             resultado_path = "imagen_resultante.png"
#             cv2.imwrite(resultado_path, resultado)
#             print('Image processed and saved successfully')

# @app.route('/')
# def index():
#     return render_template('index.html')

# if __name__ == '__main__':
#     ip_conexion = obtener_ip_conexion()
#     print('Flask server running on IP:', ip_conexion)
    
#     # Start the socket server in a separate thread
#     socket_thread = threading.Thread(target=start_socket_server)
#     socket_thread.daemon = True
#     socket_thread.start()
    
#     # Start the Flask server
#     app.run(host='0.0.0.0', port=5001)
