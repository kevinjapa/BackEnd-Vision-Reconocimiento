
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

def gafas(image, eye_coords, glasses_img):
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
            if resized_glasses[i - top_left[1], j - top_left[0], 3] > 0: 
                image[i, j] = resized_glasses[i - top_left[1], j - top_left[0]]

def nariz(image, nose_coords, nose_img, offset_y=0):
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

def bigote(image, mouth_coords, mustache_img):
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

def sombrero(image, face_coords, hat_img):
    face_x, face_y, face_w, face_h = face_coords[0]
    hat_width = face_w
    hat_height = int(hat_img.shape[0] * (hat_width / hat_img.shape[1]))
    if hat_height <= 0:
        print("Error: La altura del sombrero calculada es inválida.")
        return
    
    resized_hat = cv2.resize(hat_img, (hat_width, hat_height))
    top_left = (face_x + face_w // 2 - resized_hat.shape[1] // 2, face_y + face_h // 4 - resized_hat.shape[0])

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

def graficarPuntosRecividos(image, coords, color):
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

    image = cv2.imread("recibido/output.png", cv2.IMREAD_UNCHANGED)

    graficarPuntosRecividos(image, face_coords, (255, 0, 0))
    graficarPuntosRecividos(image, nose_coords, (0, 255, 0))
    graficarPuntosRecividos(image, mouth_coords, (0, 0, 255))
    graficarPuntosRecividos(image, eye_coords, (255, 255, 0))

    cv2.imwrite("results/Img_Reconocimiento.png", image)
    cv2.imshow("Img Reconocimiento Filtro", image)
    
    imageRecibida = cv2.imread("recibido/output.png", cv2.IMREAD_UNCHANGED)

    img_gafas= cv2.imread("assets/gafas.png", cv2.IMREAD_UNCHANGED)
    if len(eye_coords) >= 2:
        gafas(imageRecibida, eye_coords, img_gafas)

    nariz_img = cv2.imread("assets/clown_nose.png", cv2.IMREAD_UNCHANGED)
    # if nose_coords:
    nariz(imageRecibida, nose_coords, nariz_img, offset_y=-10)

    bigote_img = cv2.imread("assets/mustache.png", cv2.IMREAD_UNCHANGED)
    # if mouth_coords:
    bigote(imageRecibida, mouth_coords, bigote_img)

    sombrero_img = cv2.imread("assets/sombrero.png", cv2.IMREAD_UNCHANGED)
    # if len(face_coords) >= 1:
    sombrero(imageRecibida, face_coords, sombrero_img)

    cv2.imwrite("results/Img_Filtros.png", imageRecibida)
    cv2.imshow("Img Filtros", imageRecibida)

    print('Resultado Generado')
    print('================================================================')

    os.remove(zip_path)

    if cv2.waitKey(1) & 0xFF == ord('q'): 
        cv2.destroyAllWindows()
        break
