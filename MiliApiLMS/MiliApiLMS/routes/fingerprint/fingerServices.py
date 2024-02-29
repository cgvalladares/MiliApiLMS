from flask import jsonify, request
from PIL import Image

from MiliApiLMS.fingerprint.tools.toolsFingerprint import decrypt, encrypt, verImgPillow
from . import finger_bp
import base64
from imagehash import dhash
import ast
from datetime import datetime
import pytz
from MiliApiLMS.services.authJWT.tokekJWT import token_required


@finger_bp.route('/')
def rootFinger():
    #cryptJS='4I4xXz/IzlOajX1KcXk5Ng==FwDTlHKKvUnK2fKmHYJslg=='
    #pythonEnc=encrypt('2222')
    #print(f'encrypy Python: {pythonEnc}')
    #pythonDec=decrypt(pythonEnc)
    #print(f'decript python: {pythonDec}')
    #j='pT1V3hQbjH/JTdDjpqJFwgSmEP3ntIu8SUfztv801iM='
    #jj=decrypt(j)
    #print(f'decript JS: {jj}')
    return 'root finger'

############### busca y compra huella con las huellas registradas en formato dhash
@finger_bp.route('/comparefingerprint', methods=['POST'])
@token_required
def comparefinger():
    from MiliApiLMS.fingerprint.tools.toolsFingerprint import encontrar_coincidencias, cargar_imagen_base64
    if 'imgHuella' not in request.files:
        return jsonify({'error': 'Se requiere una imagen en la solicitud'}), 400
    huella = []
    for i, imagen in enumerate(request.files.getlist('imgHuella')):
        datos = imagen.stream.read()
        datos = base64.b64encode(datos).decode()
        huella.append({
            'imagen_{}'.format(i+1): datos
        })
    for i, imagen_base64 in enumerate(huella):
        imagen_huella = cargar_imagen_base64(imagen_base64['imagen_{}'.format(i + 1)])
    # Convertir la imagen de prueba a formato Pillow
    imagen_huella_pillow = Image.fromarray((imagen_huella[0] * 255).astype('uint8'))
    #verImgPillow(imagen_huella_pillow)
    # Calcular el hash de la imagen de prueba
    hash_prueba = dhash(imagen_huella_pillow)
    coincidencias, dedo = encontrar_coincidencias(hash_prueba)
    total=len(coincidencias)
    return jsonify({'Personas': encrypt(str(coincidencias)), 'CodigoDedo': encrypt(str(dedo)) , 'totalCoincidencias':total})

############### Agrega huella en formato dhash a la DB
@finger_bp.route('/insertfingerprint', methods=['POST'])
@token_required
def insertfinger():
    from MiliApiLMS.fingerprint.tools.toolsFingerprint import encontrar_coincidencias, cargar_imagen_base64
    from MiliApiLMS import sqlServer
    from MiliApiLMS.models.fingerprint.modelACAHuellasDactilares import ACAHuellaDactilar
    # Verificar si se recibe un JSON y una image
    if 'json' not in request.headers:
        return jsonify({'error': 'Se requiere un JSON en la solicitud'}), 400
    if 'imgHuella' not in request.files:
        return jsonify({'error': 'Se requiere una imagen en la solicitud'}), 400
    #Obtiene el json y lo convierte
    json=request.headers.get('json')
    data_json = ast.literal_eval(json)
    # Verificar que todos los campos requeridos est�n presentes en el JSON
    if not all([data_json['CodigoDedo'], data_json['CodigoPersona'], data_json['CodigoUsuario'], data_json['HuellaEsValida']]):
        return jsonify({'error': 'Faltan campos requeridos en el JSON'}), 400
    huella = []
    for i, imagen in enumerate(request.files.getlist('imgHuella')):
        datos = imagen.stream.read()
        datos = base64.b64encode(datos).decode()
        huella.append({
            'imagen_{}'.format(i+1): datos
        })
    for i, imagen_base64 in enumerate(huella):
        imagen_huella = cargar_imagen_base64(imagen_base64['imagen_{}'.format(i + 1)])
    # Convertir la imagen de prueba a formato Pillow
    imagen_huella_pillow = Image.fromarray((imagen_huella[0] * 255).astype('uint8'))
    # Calcular el hash de la imagen de prueba
    hash_imagen = dhash(imagen_huella_pillow)
    # Convierte el hash en una cadena hexadecimal y luego a bytes
    hash_bytes = bytes(str(hash_imagen), 'utf-8')
    
    # Crear una instancia del modelo con los datos recibidos
    cd=decrypt(data_json['CodigoDedo'])
    cp=decrypt(data_json['CodigoPersona'])
    cu=decrypt(data_json['CodigoUsuario'])
    print(f'cd: {cd}, cp: {cp}, cu: {cu}')
    nueva_huella = ACAHuellaDactilar(
        CodigoDedo=cd,
        CodigoPersona=cp,
        FechaRegistro=obtener_fecha_y_hora(),
        Huella=hash_bytes,
        CodigoUsuario=cu,
        HuellaEsValida=data_json['HuellaEsValida']
    )
    sqlServer.session.add(nueva_huella)
    sqlServer.session.commit()
    return jsonify({'mensaje': 'Huella guardada exitosamente'})

def obtener_fecha_y_hora():
    # Obtener la hora actual en la zona horaria UTC
    hora_utc = datetime.utcnow()
    # Convertir la hora UTC a la zona horaria de Guatemala
    zona_horaria_guatemala = pytz.timezone('America/Guatemala')
    hora_guatemala = hora_utc.replace(tzinfo=pytz.utc).astimezone(zona_horaria_guatemala)
    # Formatear la fecha y hora en un formato legible
    fecha_hora_formateada = hora_guatemala.strftime('%Y-%m-%d %H:%M:%S')
    return fecha_hora_formateada

###### test ############################################### 2024-02-15 14:52:41.570
@finger_bp.route('/gethuellas')
@token_required
def gethuellas():
    from MiliApiLMS.fingerprint.tools.toolsFingerprint import ListaHuellas
    h=ListaHuellas()
    print(h)
    return 'finger/gethuellas'

@finger_bp.route('/createhuellas')
@token_required
def createhuellas():
    from MiliApiLMS.fingerprint.tools.toolsFingerprint import CargaImg_a_db_temp
    CargaImg_a_db_temp()
    return 'finger/createhuellas'


