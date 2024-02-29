import os
from datetime import datetime
from PIL import Image, ImageFilter, ImageEnhance
from imagehash import dhash
import io
import random
from datetime import datetime
import numpy as np
from scipy.spatial import distance
import numpy as np
import base64
import matplotlib.pyplot as plt

###################### Funci�n para comparar dhashes y encontrar coincidencias
def encontrar_coincidencias(hash_prueba):
    import imagehash
    from config import Humbral
    from MiliApiLMS.models.fingerprint.modelACAHuellasDactilares import ACAHuellaDactilar
    umbral_hash = Humbral.HUMBRAL_DHASH
    coincidencias = []
    dedo=[]
    huellas = ACAHuellaDactilar.query.with_entities(ACAHuellaDactilar.Huella, ACAHuellaDactilar.CodigoPersona, ACAHuellaDactilar.CodigoDedo).all()
    for huella_registrada, codigo_persona, codigo_dedo in huellas:
        # Convertir las huellas a enteros
        hash_registrada = imagehash.hex_to_hash(huella_registrada)
        # Calcular la distancia de Hamming
        distancia =hash_prueba - hash_registrada
        if distancia < umbral_hash:
            coincidencias.append(codigo_persona)
            dedo.append(codigo_dedo)
    return coincidencias, dedo

def cargar_imagen_base64_1(base64_str):
    imagen_bytes = base64.b64decode(base64_str)
    with io.BytesIO(imagen_bytes) as f:
        imagen_pil = Image.open(f).convert('RGB')
        imagen_pil = imagen_pil.resize((360, 320))  # Redimensionar la imagen al tama�o deseado
        img_array = np.array(imagen_pil)
        img_array = img_array / 255.0  # Normalizar la imagen
        # Normalizar la imagen utilizando la media y la desviación estándar
        #img_array = (img_array - np.mean(img_array)) / np.std(img_array)
        return np.expand_dims(img_array, axis=0)
    
def cargar_imagen_base64_2(base64_str):
    size=(720, 640)
    imagen_bytes = base64.b64decode(base64_str)
    with io.BytesIO(imagen_bytes) as f:
        imagen_pil = Image.open(f).convert('L')  # Convertir a escala de grises
        # Redimensionar la imagen al tamaño deseado
        imagen_pil = imagen_pil.resize(size, Image.LANCZOS)
        # Aplicar un filtro de mejora de contraste
        enhancer = ImageEnhance.Contrast(imagen_pil)
        imagen_pil = enhancer.enhance(2)  # Ajustar el factor de contraste según sea necesario
        # Aplicar un filtro de realce de bordes
        imagen_pil = imagen_pil.filter(ImageFilter.EDGE_ENHANCE)    
        # Convertir la imagen PIL a un array numpy
        img_array = np.array(imagen_pil)  
        # Normalizar la imagen al rango [0, 1]
        img_array = img_array / 255.0   
        return np.expand_dims(img_array, axis=0)
    
def cargar_imagen_base64(base64_str):
    size=(720, 640)
    imagen_bytes = base64.b64decode(base64_str)
    
    with io.BytesIO(imagen_bytes) as f:
        imagen_pil = Image.open(f).convert('L')  # Convertir a escala de grises
        # Redimensionar la imagen al tamaño deseado
        imagen_pil = imagen_pil.resize(size, Image.LANCZOS)  
        # Aplicar un filtro de mejora de contraste
        enhancer = ImageEnhance.Contrast(imagen_pil)
        imagen_pil = enhancer.enhance(2)  # Ajustar el factor de contraste según sea necesario   
        # Aplicar un filtro de realce de bordes
        imagen_pil = imagen_pil.filter(ImageFilter.EDGE_ENHANCE)   
        # Aplicar umbralización adaptativa
        imagen_pil = imagen_pil.point(lambda p: p > 150 and 255) 
        # Aplicar un filtro de mediana para reducir el ruido
        imagen_pil = imagen_pil.filter(ImageFilter.MedianFilter(size=3))  
        # Convertir la imagen PIL a un array numpy
        img_array = np.array(imagen_pil)     
        # Normalizar la imagen al rango [0, 1]
        img_array = img_array / 255.0   
        return np.expand_dims(img_array, axis=0)
############## END Funci�n para comparar dhashes y encontrar coincidencias


################# otros 
def verImgPillow(imgPillow):# agregar a toolsfinger
    # Tama�o de las im�genes en la visualizaci�n
    tamanio_imagen = (8, 6)
    # Mostrar la imagen de prueba
    plt.figure(figsize=tamanio_imagen)
    plt.imshow(imgPillow, cmap='gray')
    plt.title('Imagen de prueba')
    plt.axis('on')
    plt.show()

#salt = b'Ivan Medvedev'
#salt = b'\x49\x76\x61\x6e\x20\x4d\x65\x64\x76\x65\x64\x65\x76' 
key = b'LecComputacionSA'
def encrypt(data):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(iv + encrypted_data).decode()

def decrypt(encrypted_data):
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size)
    return decrypted_data.decode()


######### test################################
#lista huellas
def ListaHuellas():
    from MiliApiLMS.models.fingerprint.modelACAHuellasDactilares import ACAHuellaDactilar

    huella=ACAHuellaDactilar.query.with_entities(ACAHuellaDactilar.Huella).all()
    return huella

# carga imagens dhash a DB
def CargaImg_a_db_temp():
    from MiliApiLMS.models.fingerprint.modelACAHuellasDactilares import ACAHuellaDactilar
    from MiliApiLMS import sqlServer   
    # Ruta a la carpeta img
    carpeta_img = 'MiliApiLMS/img/huellas'
    cont =0
    u=None
    # Recorre la carpeta img y sus subcarpetas
    for ruta, _, archivos in os.walk(carpeta_img):
        for archivo in archivos:
            # Solo procesa archivos de imagen (puedes ajustar seg�n los tipos de imagen que deseas procesar)
            if archivo.endswith(('.jpg', '.jpeg', '.png')):
                # Ruta completa de la imagen
                imagen_path = os.path.join(ruta, archivo)
                hash_bytes = calcular_hash(imagen_path)
                #crea usuario
                cont =cont+1
                if cont<=3:
                    u='lec_cmayorga'
                else:
                    u='lec_cvalladares'
                    cont=0
                # Guarda el registro en la base de datos
                nueva_huella = ACAHuellaDactilar(
                    CodigoDedo=random.randint(1, 10),  # Ingresa el c�digo del dedo seg�n sea necesario
                    CodigoPersona=random.randint(2345, 5412),  # Ingresa el c�digo de la persona seg�n sea necesario
                    FechaRegistro=datetime.now(),
                    Huella=hash_bytes,  # Cambiado a bytes
                    CodigoUsuario=u,  # Ingresa el c�digo del usuario seg�n sea necesario
                    HuellaEsValida=True  # Ingresa si la huella es v�lida o no seg�n sea necesario
                )
                sqlServer.session.add(nueva_huella)
    # Guarda los cambios en la base de datos
    sqlServer.session.commit()

#calcula el hash de la imagen
def calcular_hash(imagen_path):
    # Cargar la imagen
    imagen = Image.open(imagen_path)    
    # Calcular el hash de la imagen usando dhash
    hash_imagen = dhash(imagen)
    # Convierte el hash en una cadena hexadecimal y luego a bytes
    hash_bytes = bytes(str(hash_imagen), 'utf-8')
    return hash_bytes

#lista huellas y codigo persona
def ListarHuellasPersonas():
    from MiliApiLMS.models.fingerprint.modelACAHuellasDactilares import ACAHuellaDactilar

    huella=ACAHuellaDactilar.query.with_entities(ACAHuellaDactilar.Huella, ACAHuellaDactilar.CodigoPersona).all()
    return huella
