


# import socket
# import zipfile
# import os
# import cv2
# import csv

# def obtener_ip_conexion():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 1))
#         ip_address = s.getsockname()[0]
#     except Exception:
#         ip_address = '127.0.0.1'
#     return ip_address

# def add_glasses(image, eye_coords, glasses_img):
#     # Redimensionar las gafas para que coincidan con el ancho de los ojos
#     eye_width = eye_coords[1][0] - eye_coords[0][0] + eye_coords[1][2]
#     if eye_width <= 0:
#         print("Error: El ancho de los ojos calculado es inválido.")
#         return
    
#     glasses_height = int(glasses_img.shape[0] * (eye_width / glasses_img.shape[1]))
#     if glasses_height <= 0:
#         print("Error: La altura de las gafas calculada es inválida.")
#         return
    
#     resized_glasses = cv2.resize(glasses_img, (eye_width, glasses_height))

#     # Calcular el centro de los ojos
#     left_eye_center = (eye_coords[0][0] + eye_coords[0][2] // 2, eye_coords[0][1] + eye_coords[0][3] // 2)
#     right_eye_center = (eye_coords[1][0] + eye_coords[1][2] // 2, eye_coords[1][1] + eye_coords[1][3] // 2)

#     # Calcular el centro de las gafas
#     eye_center = ((left_eye_center[0] + right_eye_center[0]) // 2, (left_eye_center[1] + right_eye_center[1]) // 2)

#     # Calcular la posición superior izquierda para colocar las gafas
#     top_left = (eye_center[0] - resized_glasses.shape[1] // 2, eye_center[1] - resized_glasses.shape[0] // 2)

#     # Asegurarse de que las gafas no se salgan de los límites de la imagen
#     for i in range(resized_glasses.shape[0]):
#         for j in range(resized_glasses.shape[1]):
#             if resized_glasses[i, j, 3] > 0:  # alpha channel
#                 y, x = top_left[1] + i, top_left[0] + j
#                 if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
#                     image[y, x] = resized_glasses[i, j]

# def draw_rectangles(image, coords, color):
#     for (x, y, w, h) in coords:
#         cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

# while True:
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ('0.0.0.0', 3500)
#     print('Iniciando en {} puerto {}'.format(*server_address))
#     server_socket.bind(server_address)

#     ip_conexion = obtener_ip_conexion()
#     print('Servidor corriendo en IP:', ip_conexion)

#     server_socket.listen(1)

#     print('Esperando conexión...')
#     client_socket, client_address = server_socket.accept()
#     print('Conexión establecida desde', client_address)

#     zip_data = b''
#     while True:
#         data = client_socket.recv(1024)
#         if not data:
#             break
#         zip_data += data

#     client_socket.close()
#     server_socket.close()

#     zip_path = "data_recibido.zip"
#     with open(zip_path, "wb") as zip_file:
#         zip_file.write(zip_data)

#     print('ZIP recibido y guardado correctamente')

#     # Descomprimir el archivo ZIP
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(".")

#     print('Archivos descomprimidos')

#     # Leer el archivo CSV
#     points = {
#         'face': [],
#         'eye': [],
#         'nose': [],
#         'mouth': []
#     }

#     with open("output.csv", "r") as f:
#         reader = csv.reader(f)
#         next(reader)  # Saltar el encabezado
#         for row in reader:
#             if row[0] in points:
#                 x = int(row[1])
#                 y = int(row[2])
#                 width = int(row[3])
#                 height = int(row[4])
#                 points[row[0]].append((x, y, width, height))

#     # Filtrar los puntos: asumimos que solo necesitamos el primer punto para cada tipo excepto los ojos
#     face_coords = points['face'][:1]
#     nose_coords = points['nose'][:1]
#     mouth_coords = points['mouth'][:1]
#     eye_coords = points['eye'][:2]

#     # Leer la imagen
#     image_path = "output.png"
#     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

#     # Dibujar rectángulos en la imagen original
#     draw_rectangles(image, face_coords, (255, 0, 0))
#     draw_rectangles(image, nose_coords, (0, 255, 0))
#     draw_rectangles(image, mouth_coords, (0, 0, 255))
#     draw_rectangles(image, eye_coords, (255, 255, 0))

#     # Guardar la imagen con los rectángulos dibujados
#     cv2.imwrite("output_with_rectangles.png", image)
#     cv2.imshow("cuadrados",image)
    
#     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
#     # Verificar la existencia del archivo gafas.png
#     glasses_img_path = "gafas.png"
#     if not os.path.exists(glasses_img_path):
#         print(f"Error: {glasses_img_path} no existe.")
#         exit(1)

#     glasses_img = cv2.imread(glasses_img_path, cv2.IMREAD_UNCHANGED)
#     if glasses_img is None:
#         print(f"Error: No se pudo leer {glasses_img_path}. Verifique que el archivo es accesible y es una imagen válida.")
#         exit(1)

#     if len(eye_coords) >= 2:
#         # Suponemos que los dos primeros son los ojos
#         add_glasses(image, eye_coords, glasses_img)

#     # Guardar la nueva imagen con gafas
#     cv2.imwrite("output_with_glasses.png", image)
#     cv2.imshow("Gafas",image)

#     print('Imagen con gafas guardada correctamente')

#     os.remove(zip_path)

#     if cv2.waitKey(1) & 0xFF == ord('q'): 
#                 cv2.destroyAllWindows()
#                 break








# import socket
# import zipfile
# import os
# import cv2
# import csv

# def obtener_ip_conexion():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 1))
#         ip_address = s.getsockname()[0]
#     except Exception:
#         ip_address = '127.0.0.1'
#     return ip_address

# def add_glasses(image, eye_coords, glasses_img):
#     eye_width = eye_coords[1][0] - eye_coords[0][0] + eye_coords[1][2]
#     if eye_width <= 0:
#         print("Error: El ancho de los ojos calculado es inválido.")
#         return
    
#     glasses_height = int(glasses_img.shape[0] * (eye_width / glasses_img.shape[1]))
#     if glasses_height <= 0:
#         print("Error: La altura de las gafas calculada es inválida.")
#         return
    
#     resized_glasses = cv2.resize(glasses_img, (eye_width, glasses_height))

#     left_eye_center = (eye_coords[0][0] + eye_coords[0][2] // 2, eye_coords[0][1] + eye_coords[0][3] // 2)
#     right_eye_center = (eye_coords[1][0] + eye_coords[1][2] // 2, eye_coords[1][1] + eye_coords[1][3] // 2)

#     eye_center = ((left_eye_center[0] + right_eye_center[0]) // 2, (left_eye_center[1] + right_eye_center[1]) // 2)

#     top_left = (eye_center[0] - resized_glasses.shape[1] // 2, eye_center[1] - resized_glasses.shape[0] // 2)

#     for i in range(resized_glasses.shape[0]):
#         for j in range(resized_glasses.shape[1]):
#             if resized_glasses[i, j, 3] > 0:  # alpha channel
#                 y, x = top_left[1] + i, top_left[0] + j
#                 if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
#                     image[y, x] = resized_glasses[i, j]

# def add_hat(image, face_coords, hat_img):
#     face_x, face_y, face_w, face_h = face_coords[0]
#     hat_width = face_w
#     hat_height = int(hat_img.shape[0] * (hat_width / hat_img.shape[1]))
    
#     if hat_height <= 0:
#         print("Error: La altura del sombrero calculada es inválida.")
#         return
    
#     resized_hat = cv2.resize(hat_img, (hat_width, hat_height))

#     top_left = (face_x + face_w // 2 - resized_hat.shape[1] // 2, face_y - resized_hat.shape[0])

#     for i in range(resized_hat.shape[0]):
#         for j in range(resized_hat.shape[1]):
#             if resized_hat[i, j, 3] > 0:  # alpha channel
#                 y, x = top_left[1] + i, top_left[0] + j
#                 if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
#                     image[y, x] = resized_hat[i, j]

# def draw_rectangles(image, coords, color):
#     for (x, y, w, h) in coords:
#         cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

# while True:
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ('0.0.0.0', 3500)
#     print('Iniciando en {} puerto {}'.format(*server_address))
#     server_socket.bind(server_address)

#     ip_conexion = obtener_ip_conexion()
#     print('Servidor corriendo en IP:', ip_conexion)

#     server_socket.listen(1)

#     print('Esperando conexión...')
#     client_socket, client_address = server_socket.accept()
#     print('Conexión establecida desde', client_address)

#     zip_data = b''
#     while True:
#         data = client_socket.recv(1024)
#         if not data:
#             break
#         zip_data += data

#     client_socket.close()
#     server_socket.close()

#     zip_path = "data_recibido.zip"
#     with open(zip_path, "wb") as zip_file:
#         zip_file.write(zip_data)

#     print('ZIP recibido y guardado correctamente')

#     # Descomprimir el archivo ZIP
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(".")

#     print('Archivos descomprimidos')

#     # Leer el archivo CSV
#     points = {
#         'face': [],
#         'eye': [],
#         'nose': [],
#         'mouth': []
#     }

#     with open("output.csv", "r") as f:
#         reader = csv.reader(f)
#         next(reader)  # Saltar el encabezado
#         for row in reader:
#             if row[0] in points:
#                 x = int(row[1])
#                 y = int(row[2])
#                 width = int(row[3])
#                 height = int(row[4])
#                 points[row[0]].append((x, y, width, height))

#     face_coords = points['face'][:1]
#     nose_coords = points['nose'][:1]
#     mouth_coords = points['mouth'][:1]
#     eye_coords = points['eye'][:2]

#     image_path = "output.png"
#     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

#     draw_rectangles(image, face_coords, (255, 0, 0))
#     draw_rectangles(image, nose_coords, (0, 255, 0))
#     draw_rectangles(image, mouth_coords, (0, 0, 255))
#     draw_rectangles(image, eye_coords, (255, 255, 0))

#     cv2.imwrite("output_with_rectangles.png", image)
#     cv2.imshow("cuadrados",image)
    
#     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
#     glasses_img_path = "gafas.png"
#     if not os.path.exists(glasses_img_path):
#         print(f"Error: {glasses_img_path} no existe.")
#         exit(1)

#     glasses_img = cv2.imread(glasses_img_path, cv2.IMREAD_UNCHANGED)
#     if glasses_img is None:
#         print(f"Error: No se pudo leer {glasses_img_path}. Verifique que el archivo es accesible y es una imagen válida.")
#         exit(1)

#     if len(eye_coords) >= 2:
#         add_glasses(image, eye_coords, glasses_img)

#     hat_img_path = "sombrero.png"
#     if not os.path.exists(hat_img_path):
#         print(f"Error: {hat_img_path} no existe.")
#         exit(1)

#     hat_img = cv2.imread(hat_img_path, cv2.IMREAD_UNCHANGED)
#     if hat_img is None:
#         print(f"Error: No se pudo leer {hat_img_path}. Verifique que el archivo es accesible y es una imagen válida.")
#         exit(1)

#     if len(face_coords) >= 1:
#         add_hat(image, face_coords, hat_img)

#     cv2.imwrite("output_with_glasses_and_hat.png", image)
#     cv2.imshow("Gafas y Sombrero", image)

#     print('Imagen con gafas y sombrero guardada correctamente')

#     os.remove(zip_path)

#     if cv2.waitKey(1) & 0xFF == ord('q'): 
#                 cv2.destroyAllWindows()
#                 break

# =====================================

# import socket
# import zipfile
# import os
# import cv2
# import csv

# def obtener_ip_conexion():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 1))
#         ip_address = s.getsockname()[0]
#     except Exception:
#         ip_address = '127.0.0.1'
#     return ip_address

# def add_glasses(image, eye_coords, glasses_img):
#     eye_width = eye_coords[1][0] - eye_coords[0][0] + eye_coords[1][2]
#     if eye_width <= 0:
#         print("Error: El ancho de los ojos calculado es inválido.")
#         return
    
#     glasses_height = int(glasses_img.shape[0] * (eye_width / glasses_img.shape[1]))
#     if glasses_height <= 0:
#         print("Error: La altura de las gafas calculada es inválida.")
#         return
    
#     resized_glasses = cv2.resize(glasses_img, (eye_width, glasses_height))

#     left_eye_center = (eye_coords[0][0] + eye_coords[0][2] // 2, eye_coords[0][1] + eye_coords[0][3] // 2)
#     right_eye_center = (eye_coords[1][0] + eye_coords[1][2] // 2, eye_coords[1][1] + eye_coords[1][3] // 2)

#     eye_center = ((left_eye_center[0] + right_eye_center[0]) // 2, (left_eye_center[1] + right_eye_center[1]) // 2)

#     top_left = (eye_center[0] - resized_glasses.shape[1] // 2, eye_center[1] - resized_glasses.shape[0] // 2)

#     for i in range(resized_glasses.shape[0]):
#         for j in range(resized_glasses.shape[1]):
#             if resized_glasses[i, j, 3] > 0:  # alpha channel
#                 y, x = top_left[1] + i, top_left[0] + j
#                 if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
#                     image[y, x] = resized_glasses[i, j]

# def add_clown_nose(image, nose_coords, nose_img, offset_y=0):
#     if not nose_coords:
#         print("Error: No se detectó la nariz.")
#         return

#     (x, y, w, h) = nose_coords[0]

#     resized_nose = cv2.resize(nose_img, (w, h))

#     for i in range(resized_nose.shape[0]):
#         for j in range(resized_nose.shape[1]):
#             if resized_nose[i, j, 3] > 0:  # alpha channel
#                 y_offset, x_offset = y + i + offset_y, x + j
#                 if 0 <= y_offset < image.shape[0] and 0 <= x_offset < image.shape[1]:
#                     image[y_offset, x_offset] = resized_nose[i, j]

# def add_mustache(image, mouth_coords, mustache_img):
#     if not mouth_coords:
#         print("Error: No se detectó la boca.")
#         return

#     (x, y, w, h) = mouth_coords[0]

#     resized_mustache = cv2.resize(mustache_img, (w, int(h / 2)))  # Ajustar la altura del bigote

#     for i in range(resized_mustache.shape[0]):
#         for j in range(resized_mustache.shape[1]):
#             if resized_mustache[i, j, 3] > 0:  # alpha channel
#                 y_offset, x_offset = y + i - int(h / 2), x + j  # Ajustar el bigote para que se coloque sobre la boca
#                 if 0 <= y_offset < image.shape[0] and 0 <= x_offset < image.shape[1]:
#                     image[y_offset, x_offset] = resized_mustache[i, j]

# def draw_rectangles(image, coords, color):
#     for (x, y, w, h) in coords:
#         cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

# while True:
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_address = ('0.0.0.0', 3500)
#     print('Iniciando en {} puerto {}'.format(*server_address))
#     server_socket.bind(server_address)

#     ip_conexion = obtener_ip_conexion()
#     print('Servidor corriendo en IP:', ip_conexion)

#     server_socket.listen(1)

#     print('Esperando conexión...')
#     client_socket, client_address = server_socket.accept()
#     print('Conexión establecida desde', client_address)

#     zip_data = b''
#     while True:
#         data = client_socket.recv(1024)
#         if not data:
#             break
#         zip_data += data

#     client_socket.close()
#     server_socket.close()

#     zip_path = "data_recibido.zip"
#     with open(zip_path, "wb") as zip_file:
#         zip_file.write(zip_data)

#     print('ZIP recibido y guardado correctamente')

#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(".")

#     print('Archivos descomprimidos')

#     points = {
#         'face': [],
#         'eye': [],
#         'nose': [],
#         'mouth': []
#     }

#     with open("output.csv", "r") as f:
#         reader = csv.reader(f)
#         next(reader)  # Saltar el encabezado
#         for row in reader:
#             if row[0] in points:
#                 x = int(row[1])
#                 y = int(row[2])
#                 width = int(row[3])
#                 height = int(row[4])
#                 points[row[0]].append((x, y, width, height))

#     face_coords = points['face'][:1]
#     nose_coords = points['nose'][:1]
#     mouth_coords = points['mouth'][:1]
#     eye_coords = points['eye'][:2]

#     image_path = "output.png"
#     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

#     draw_rectangles(image, face_coords, (255, 0, 0))
#     draw_rectangles(image, nose_coords, (0, 255, 0))
#     draw_rectangles(image, mouth_coords, (0, 0, 255))
#     draw_rectangles(image, eye_coords, (255, 255, 0))

#     cv2.imwrite("output_with_rectangles.png", image)
#     cv2.imshow("cuadrados", image)
    
#     image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

#     glasses_img_path = "gafas.png"
#     if not os.path.exists(glasses_img_path):
#         print(f"Error: {glasses_img_path} no existe.")
#         exit(1)

#     glasses_img = cv2.imread(glasses_img_path, cv2.IMREAD_UNCHANGED)
#     if glasses_img is None:
#         print(f"Error: No se pudo leer {glasses_img_path}. Verifique que el archivo es accesible y es una imagen válida.")
#         exit(1)

#     if len(eye_coords) >= 2:
#         add_glasses(image, eye_coords, glasses_img)

#     nose_img_path = "clown_nose.png"
#     if not os.path.exists(nose_img_path):
#         print(f"Error: {nose_img_path} no existe.")
#         exit(1)

#     nose_img = cv2.imread(nose_img_path, cv2.IMREAD_UNCHANGED)
#     if nose_img is None:
#         print(f"Error: No se pudo leer {nose_img_path}. Verifique que el archivo es accesible y es una imagen válida.")
#         exit(1)

#     if nose_coords:
#         add_clown_nose(image, nose_coords, nose_img, offset_y=-10)

#     mustache_img_path = "mustache.png"
#     if not os.path.exists(mustache_img_path):
#         print(f"Error: {mustache_img_path} no existe.")
#         exit(1)

#     mustache_img = cv2.imread(mustache_img_path, cv2.IMREAD_UNCHANGED)
#     if mustache_img is None:
#         print(f"Error: No se pudo leer {mustache_img_path}. Verifique que el archivo es accesible y es una imagen válida.")
#         exit(1)

#     if mouth_coords:
#         add_mustache(image, mouth_coords, mustache_img)

#     cv2.imwrite("output_with_glasses_nose_mustache.png", image)
#     cv2.imshow("Gafas, Nariz de Payaso y Bigote", image)

#     print('Imagen con gafas, nariz de payaso y bigote guardada correctamente')

#     os.remove(zip_path)

#     if cv2.waitKey(1) & 0xFF == ord('q'): 
#         cv2.destroyAllWindows()
#         break





import socket
import zipfile
import os
import cv2
import csv

def obtener_ip_conexion():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 1))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    return ip_address

# def add_glasses(image, eye_coords, glasses_img):
#     eye_width = eye_coords[1][0] - eye_coords[0][0] + eye_coords[1][2]
#     if eye_width <= 0:
#         print("Error: El ancho de los ojos calculado es inválido.")
#         return
    
#     glasses_height = int(glasses_img.shape[0] * (eye_width / glasses_img.shape[1]))
#     if glasses_height <= 0:
#         print("Error: La altura de las gafas calculada es inválida.")
#         return
    
#     resized_glasses = cv2.resize(glasses_img, (eye_width, glasses_height))

#     left_eye_center = (eye_coords[0][0] + eye_coords[0][2] // 2, eye_coords[0][1] + eye_coords[0][3] // 2)
#     right_eye_center = (eye_coords[1][0] + eye_coords[1][2] // 2, eye_coords[1][1] + eye_coords[1][3] // 2)

#     eye_center = ((left_eye_center[0] + right_eye_center[0]) // 2, (left_eye_center[1] + right_eye_center[1]) // 2)

#     top_left = (eye_center[0] - resized_glasses.shape[1] // 2, eye_center[1] - resized_glasses.shape[0] // 2)

#     for i in range(resized_glasses.shape[0]):
#         for j in range(resized_glasses.shape[1]):
#             if resized_glasses[i, j, 3] > 0:  # alpha channel
#                 y, x = top_left[1] + i, top_left[0] + j
#                 if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
#                     image[y, x] = resized_glasses[i, j]

def add_glasses(image, eye_coords, glasses_img):
    # Calcular el ancho de las gafas en función de la distancia entre los ojos
    eye_width = eye_coords[1][0] - eye_coords[0][0] + eye_coords[1][2]
    if eye_width <= 0:
        print("Error: El ancho de los ojos calculado es inválido.")
        return
    
    # Calcular la altura de las gafas manteniendo la proporción original
    glasses_height = int(glasses_img.shape[0] * (eye_width / glasses_img.shape[1]))
    if glasses_height <= 0:
        print("Error: La altura de las gafas calculada es inválida.")
        return
    
    # Redimensionar la imagen de las gafas
    resized_glasses = cv2.resize(glasses_img, (eye_width, glasses_height), interpolation=cv2.INTER_AREA)
    
    # Calcular el centro de cada ojo
    left_eye_center = (eye_coords[0][0] + eye_coords[0][2] // 2, eye_coords[0][1] + eye_coords[0][3] // 2)
    right_eye_center = (eye_coords[1][0] + eye_coords[1][2] // 2, eye_coords[1][1] + eye_coords[1][3] // 2)
    
    # Calcular el centro entre los dos ojos
    eye_center = ((left_eye_center[0] + right_eye_center[0]) // 2, (left_eye_center[1] + right_eye_center[1]) // 2)
    
    # Calcular la posición superior izquierda donde se colocarán las gafas
    top_left = (eye_center[0] - resized_glasses.shape[1] // 2, eye_center[1] - resized_glasses.shape[0] // 2)
    
    # Verificar y ajustar los bordes para no salir del límite de la imagen
    top_left = (max(top_left[0], 0), max(top_left[1], 0))
    bottom_right = (min(top_left[0] + resized_glasses.shape[1], image.shape[1]), 
                    min(top_left[1] + resized_glasses.shape[0], image.shape[0]))
    
    # Añadir las gafas a la imagen, considerando el canal alfa (transparencia)
    for i in range(top_left[1], bottom_right[1]):
        for j in range(top_left[0], bottom_right[0]):
            if resized_glasses[i - top_left[1], j - top_left[0], 3] > 0:  # Comprobar canal alfa
                image[i, j] = resized_glasses[i - top_left[1], j - top_left[0]]

def add_clown_nose(image, nose_coords, nose_img, offset_y=0):
    if not nose_coords:
        print("Error: No se detectó la nariz.")
        return

    (x, y, w, h) = nose_coords[0]

    resized_nose = cv2.resize(nose_img, (w, h))

    for i in range(resized_nose.shape[0]):
        for j in range(resized_nose.shape[1]):
            if resized_nose[i, j, 3] > 0:  # alpha channel
                y_offset, x_offset = y + i + offset_y, x + j
                if 0 <= y_offset < image.shape[0] and 0 <= x_offset < image.shape[1]:
                    image[y_offset, x_offset] = resized_nose[i, j]

def add_mustache(image, mouth_coords, mustache_img):
    if not mouth_coords:
        print("Error: No se detectó la boca.")
        return

    (x, y, w, h) = mouth_coords[0]

    # Redimensionar el bigote para que sea del mismo ancho que la boca
    resized_mustache = cv2.resize(mustache_img, (w, int(h / 2)))

    # Calcular la posición del bigote para que esté más arriba dentro del borde superior interno de la boca
    mustache_y_offset = y - int(h / 4)  # Ajuste para colocar el bigote más arriba

    for i in range(resized_mustache.shape[0]):
        for j in range(resized_mustache.shape[1]):
            if resized_mustache[i, j, 3] > 0:  # canal alpha
                y_offset, x_offset = mustache_y_offset + i, x + j
                if 0 <= y_offset < image.shape[0] and 0 <= x_offset < image.shape[1]:
                    image[y_offset, x_offset] = resized_mustache[i, j]

# def add_hat(image, face_coords, hat_img):
#     face_x, face_y, face_w, face_h = face_coords[0]
#     hat_width = face_w
#     hat_height = int(hat_img.shape[0] * (hat_width / hat_img.shape[1]))
    
#     if hat_height <= 0:
#         print("Error: La altura del sombrero calculada es inválida.")
#         return
    
#     resized_hat = cv2.resize(hat_img, (hat_width, hat_height))

#     top_left = (face_x + face_w // 2 - resized_hat.shape[1] // 2, face_y - resized_hat.shape[0])

#     for i in range(resized_hat.shape[0]):
#         for j in range(resized_hat.shape[1]):
#             if resized_hat[i, j, 3] > 0:  # alpha channel
#                 y, x = top_left[1] + i, top_left[0] + j
#                 if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
#                     image[y, x] = resized_hat[i, j]


def add_hat(image, face_coords, hat_img):
    face_x, face_y, face_w, face_h = face_coords[0]
    hat_width = face_w
    hat_height = int(hat_img.shape[0] * (hat_width / hat_img.shape[1]))
    
    if hat_height <= 0:
        print("Error: La altura del sombrero calculada es inválida.")
        return
    
    resized_hat = cv2.resize(hat_img, (hat_width, hat_height))
    
    # Calcular la posición superior izquierda del sombrero
    top_left = (face_x + face_w // 2 - resized_hat.shape[1] // 2, face_y - resized_hat.shape[0])
    
    # Asegurarse de que el sombrero no salga de los bordes superiores de la imagen
    if top_left[1] < 0:
        print("Error: El sombrero sale de los bordes superiores de la imagen.")
        return

    for i in range(resized_hat.shape[0]):
        for j in range(resized_hat.shape[1]):
            if resized_hat[i, j, 3] > 0:  # alpha channel
                y, x = top_left[1] + i, top_left[0] + j
                if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                    image[y, x] = resized_hat[i, j]



def draw_rectangles(image, coords, color):
    for (x, y, w, h) in coords:
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)

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

    zip_data = b''
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        zip_data += data

    client_socket.close()
    server_socket.close()

    zip_path = "recibido/data_recibido.zip"
    with open(zip_path, "wb") as zip_file:
        zip_file.write(zip_data)

    print('ZIP recibido y guardado correctamente')

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # zip_ref.extractall(".")
        zip_ref.extractall("recibido/")

    print('Archivos descomprimidos')

    points = {
        'face': [],
        'eye': [],
        'nose': [],
        'mouth': []
    }

    with open("recibido/output.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)  # Saltar el encabezado
        for row in reader:
            if row[0] in points:
                x = int(row[1])
                y = int(row[2])
                width = int(row[3])
                height = int(row[4])
                points[row[0]].append((x, y, width, height))

    face_coords = points['face'][:1]
    nose_coords = points['nose'][:1]
    mouth_coords = points['mouth'][:1]
    eye_coords = points['eye'][:2]

    image_path = "recibido/output.png"
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    draw_rectangles(image, face_coords, (255, 0, 0))
    draw_rectangles(image, nose_coords, (0, 255, 0))
    draw_rectangles(image, mouth_coords, (0, 0, 255))
    draw_rectangles(image, eye_coords, (255, 255, 0))

    cv2.imwrite("results/Img_Reconocimiento.png", image)
    cv2.imshow("Img Reconocimiento Filtro", image)
    
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    glasses_img_path = "assets/gafas.png"
    if not os.path.exists(glasses_img_path):
        print(f"Error: {glasses_img_path} no existe.")
        exit(1)

    glasses_img = cv2.imread(glasses_img_path, cv2.IMREAD_UNCHANGED)
    if glasses_img is None:
        print(f"Error: No se pudo leer {glasses_img_path}. imagen válida.")
        exit(1)

    if len(eye_coords) >= 2:
        add_glasses(image, eye_coords, glasses_img)

    nose_img_path = "assets/clown_nose.png"
    if not os.path.exists(nose_img_path):
        print(f"Error: {nose_img_path} no existe.")
        exit(1)

    nose_img = cv2.imread(nose_img_path, cv2.IMREAD_UNCHANGED)
    if nose_img is None:
        print(f"Error: No se pudo leer {nose_img_path}. imagen válida.")
        exit(1)

    if nose_coords:
        add_clown_nose(image, nose_coords, nose_img, offset_y=-10)

    mustache_img_path = "assets/mustache.png"
    if not os.path.exists(mustache_img_path):
        print(f"Error: {mustache_img_path} no existe.")
        exit(1)

    mustache_img = cv2.imread(mustache_img_path, cv2.IMREAD_UNCHANGED)
    if mustache_img is None:
        print(f"Error: No se pudo leer {mustache_img_path}. imagen válida.")
        exit(1)

    if mouth_coords:
        add_mustache(image, mouth_coords, mustache_img)

    hat_img_path = "assets/sombrero.png"
    if not os.path.exists(hat_img_path):
        print(f"Error: {hat_img_path} no existe.")
        exit(1)

    hat_img = cv2.imread(hat_img_path, cv2.IMREAD_UNCHANGED)
    if hat_img is None:
        print(f"Error: No se pudo leer {hat_img_path}. imagen válida.")
        exit(1)
    if len(face_coords) >= 1:
         add_hat(image, face_coords, hat_img)

    cv2.imwrite("results/Img_Filtros.png", image)
    cv2.imshow("Img Filtros", image)

    print('Resultado Generado')
    print('================================================================')

    os.remove(zip_path)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        cv2.destroyAllWindows()
        break
