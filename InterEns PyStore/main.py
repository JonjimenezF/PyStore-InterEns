from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_mail import Mail, Message
import os
import uuid 
import requests
import json
import traceback
# import supabase

app = Flask(__name__)
from flask_cors import CORS

CORS(app)


URL_SUPEBASE = 'https://gglsaoykhjniypthjgfc.supabase.co/rest/v1/'
supebaseheads = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbHNhb3lraGpuaXlwdGhqZ2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ1NTIwMTQsImV4cCI6MjAzMDEyODAxNH0.jmngoEfB87raLwTHDq1DI347a4owyHCqs75VSJUwMZo'
# os.environ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbHNhb3lraGpuaXlwdGhqZ2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ1NTIwMTQsImV4cCI6MjAzMDEyODAxNH0.jmngoEfB87raLwTHDq1DI347a4owyHCqs75VSJUwMZo'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbHNhb3lraGpuaXlwdGhqZ2ZjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNDU1MjAxNCwiZXhwIjoyMDMwMTI4MDE0fQ.FTBFPMMnJOACE2iYWt47XaTF8_wjD0anXfyrVEPV74k'
# supabase_anon_key = os.getenv('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbHNhb3lraGpuaXlwdGhqZ2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ1NTIwMTQsImV4cCI6MjAzMDEyODAxNH0.jmngoEfB87raLwTHDq1DI347a4owyHCqs75VSJUwMZo')
    

#---------------------------------------------------TABLA PRODUCTO--------------------------------------------------
@app.route('/obtener_productos', methods=['GET'])
def obtener_productos():
    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'PRODUCTO?select=*', headers=headers)
    return response.json(), response.status_code

@app.route('/obtener_productos_id', methods=['GET'])
def obtener_productos_id():
    id_usuario = request.args.get('id_usuario')  # Obtener el id_usuario de los parámetros de la solicitud
    headers = {'apikey': supebaseheads}
    # Ajustar la consulta para filtrar por id_usuario
    response = requests.get(URL_SUPEBASE + f"PRODUCTO?select=*&id_usuario=eq.{id_usuario}", headers=headers)
    return response.json(), response.status_code

#Eliminar
@app.route('/Eliminarproducto/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    headers = {'apikey': supebaseheads}
    
    # Primero, obtener todas las imágenes asociadas al producto
    response_imagenes = requests.get(URL_SUPEBASE + f'IMAGEN_PRODUCTO?id_producto=eq.{id}', headers=headers)
    
    if response_imagenes.status_code != 200:
        return jsonify({'error': 'Error al obtener las imágenes asociadas al producto'}), response_imagenes.status_code

    # Convertir la respuesta a formato JSON
    imagenes = response_imagenes.json()

    # Eliminar cada imagen asociada al producto
    for imagen in imagenes:
        # Verificar si la clave 'id_imagen_producto' está presente en el diccionario imagen
        if 'id_imagen_producto' in imagen:
            imagen_id = imagen['id_imagen_producto']
            print(f"Eliminando imagen con ID: {imagen_id}")
            response_delete_imagen = requests.delete(URL_SUPEBASE + f'IMAGEN_PRODUCTO?id_imagen_producto=eq.{imagen_id}', headers=headers)
            
            if response_delete_imagen.status_code != 204:
                return jsonify({'error': 'Error al eliminar una imagen asociada al producto'}), response_delete_imagen.status_code
        else:
            # Si la clave 'id_imagen_producto' no está presente en el diccionario imagen, mostrar un mensaje de error
            return jsonify({'error': 'No se encontró la clave "id_imagen_producto" en la respuesta de la imagen asociada al producto'}), 500

    # Una vez eliminadas las imágenes, eliminar el producto
    response_delete_producto = requests.delete(URL_SUPEBASE + f'PRODUCTO?id_producto=eq.{id}', headers=headers)

    if response_delete_producto.status_code == 204:
        return jsonify({'message': 'Producto y sus imágenes asociadas eliminados correctamente'}), 200
    else:
        return jsonify({'error': 'Error al eliminar el producto'}), response_delete_producto.status_code
        
@app.route('/producto/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    producto = request.json
    headers = {'apikey': supebaseheads}
    print(id)
    print("Datos recibidos:", producto)
    response = requests.put(URL_SUPEBASE + f'PRODUCTO?id_producto=eq.{id}', json=producto, headers=headers)
    print("Respuesta de Supabase:", response.status_code, response.text)
    if response.status_code == 204:
        return jsonify({'message': 'Producto actualizado correctamente'}), 200
    else:
        return jsonify({'error': 'Error al actualizar el producto'}), response.status_code

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    producto = request.json
    headers = {'apikey': supebaseheads}
    # Convertimos el objeto producto a JSON antes de pasarlo a requests.post
    response = requests.post(URL_SUPEBASE + 'PRODUCTO?', json=producto, headers=headers)
     # Verificamos si la respuesta del servidor es válida
    print(response)
    if response.status_code == 201:
        try:
            # Intentamos obtener el JSON de la respuesta
            data = producto_max_id()
        except json.decoder.JSONDecodeError:
            # Si hay un error al decodificar el JSON, devolvemos un mensaje de error genérico
            return jsonify({'error': 'Error al procesar la respuesta del servidor'}), 500

        # Verificamos si la solicitud fue exitosa
        if response.ok:
            return jsonify(data), response.status_code
        else:
            # Si la solicitud no fue exitosa, devolvemos los detalles del error
            return jsonify({'error': data}), response.status_code
    else:
        # Si la respuesta del servidor no es válida, devolvemos un mensaje de error
        return jsonify({'error': 'Error en la respuesta del servidor'}), response.status_code


def producto_max_id():
    query = {
        "select": "*",
        "order": "id_producto.desc",
        "limit": 1
    }
    headers = {'apikey': supebaseheads}
    
    response = requests.get(f'{URL_SUPEBASE}PRODUCTO', headers=headers, params=query)
    
    if response.status_code == 200:
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            return jsonify({'error': 'Error al procesar la respuesta del servidor'}), 500
        
        return data[0]
    else:
        return jsonify({'error': 'Error en la respuesta del servidor'}), response.status_code
    

    
@app.route('/obtener_productos_carrito', methods=['GET'])
def obtener_producto_carrito():
    id_producto = request.args.get('id_producto')  # Obtener el ID del usuario de los parámetros de consulta
    if id_producto is None:
        return jsonify({'error': 'Se requiere el parámetro id_usuario'}), 400
    query = {
        "select": "*",
        "id_producto": "eq." + id_producto  # Filtrar por el id_usuario específico
    }
    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'PRODUCTO?', headers=headers, params=query)
    return response.json(), response.status_code



#--------------------------------------------------TABLA CARRITO--------------------------------------------------
@app.route('/agregar_carrito', methods=['POST'])
def agregar_carrito():
    infoCarrito = request.json
    headers = {'apikey': supebaseheads}
    
    # Enviar solicitud a Supabase
    response = requests.post(URL_SUPEBASE + 'CARRITO', json=infoCarrito, headers=headers)
    
    # Verifica si la respuesta del servidor es exitosa (código 201)
    if response.status_code == 201:
        # Si la respuesta es exitosa, devuelve un mensaje de éxito
        return jsonify({'message': 'Producto agregado al carrito correctamente'}), 200
    else:
        # Si la respuesta es un error, devuelve un mensaje de error con el código de estado
        return jsonify({'error': 'Error al agregar el producto al carrito'}), response.status_code


@app.route('/eliminar_producto_carrito/<int:id_carrito>', methods=['DELETE'])
def eliminar_producto_carrito(id_carrito):
    headers = {'apikey': supebaseheads}
    
    # Aquí debes realizar la lógica para eliminar el producto del carrito
    response = requests.delete(URL_SUPEBASE + f'CARRITO?id_carrito=eq.{id_carrito}', headers=headers)
    
    if response.status_code == 204:
        return jsonify({'message': 'Producto eliminado del carrito correctamente'}), 200
    else:
        return jsonify({'error': 'Error al eliminar el producto del carrito'}), response.status_code


# Obtener todos los productos de Supabase
@app.route('/obtener_carrito', methods=['GET'])
def obtener_carrito():
    id_usuario = request.args.get('id_usuario')  # Obtener el ID del usuario de los parámetros de consulta
    if id_usuario is None:
        return jsonify({'error': 'Se requiere el parámetro id_usuario'}), 400

    # Construir la consulta para obtener todos los datos del carrito del usuario especificado
    query = {
        "select": "*",
        "id_usuario": "eq." + id_usuario  # Filtrar por el id_usuario específico
    }
    # Definir los encabezados para la solicitud a Supabase
    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'CARRITO', headers=headers, params=query)
    return response.json(), response.status_code




#--------------------------------------------------TABLA IMAGEN_PRODUCT----------------------------------------------
@app.route('/obtener_imagen', methods=['GET'])
def obtener_imagen():
    id_producto = request.args.get('id_producto')
    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'IMAGEN_PRODUCTO?id_producto=eq.' + id_producto + '&orden=eq.0', headers=headers)
    if response.status_code == 200:
        return response.json(), response.status_code
    else:
        return jsonify({'error': 'Error en el servidor'}), 500
    
@app.route('/obtener_todas_imagen', methods=['GET'])
def obtener_todas_imagen():
    query = {
        "order": "orden.asc",
    }
    id_producto = request.args.get('id_producto')
    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'IMAGEN_PRODUCTO?id_producto=eq.' + id_producto, headers=headers, params=query)
    if response.status_code == 200:
        return response.json(), response.status_code
    else:
        return jsonify({'error': 'Error en el servidor'}), 500

def subir_image_producto_max_id():
    query = {
        "select": "*",
        "order": "id_producto.desc",
        "limit": 1
    }
    headers = {'apikey': supebaseheads}
    
    response = requests.get(f'{URL_SUPEBASE}IMAGEN_PRODUCTO', headers=headers, params=query)
    
    if response.status_code == 200:
        try:
            data = response.json()
        except json.decoder.JSONDecodeError:
            return jsonify({'error': 'Error al procesar la respuesta del servidor'}), 500
        
        return data
    else:
        return jsonify({'error': 'Error en la respuesta del servidor'}), response.status_code



app.config['UPLOAD_FOLDER'] = 'upload'  # Carpeta donde se almacenan las imágenes subidas
# Lista de extensiones permitidas
extensiones_permitidas = {'jpg', 'jpeg', 'png', 'gif'}

@app.route('/subir_imagen_producto', methods=['POST'])
def subir_imagen_producto():
    producto = request.json
    headers = {'apikey': supebaseheads}
    producto = request.json   
    response = requests.post(URL_SUPEBASE + 'IMAGEN_PRODUCTO', json=producto, headers=headers)
        
    if response.status_code == 201:
        try:
            # Intentamos obtener el JSON de la respuesta
            data = subir_image_producto_max_id()
        except json.decoder.JSONDecodeError:
            # Si hay un error al decodificar el JSON, devolvemos un mensaje de error genérico
            return jsonify({'error': 'Error al procesar la respuesta del servidor'}), 500

        # Verificamos si la solicitud fue exitosa
        if response.ok:
            return jsonify(data), response.status_code
        else:
            # Si la solicitud no fue exitosa, devolvemos los detalles del error
            return jsonify({'error': data}), response.status_code
    else:
        # Si la respuesta del servidor no es válida, devolvemos un mensaje de error
        return jsonify({'error': 'Error en la respuesta del servidor'}), response.status_code
    

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'USUARIO?email=eq.' + email + '&password=eq.' + password, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        if len(user_data) == 1:
            # Usuario autenticado correctamente
            return jsonify(user_data[0]), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
    else:
        return jsonify({'error': 'Error en el servidor'}), 500

# Subir foto
@app.route('/upload', methods=['POST'])
def subir_foto():
    if 'foto' not in request.files:
        return jsonify({'error': 'No se encontró ninguna foto en la solicitud'}), 400
    
    foto = request.files['foto']
    if foto.filename == '':
        return jsonify({'error': 'Nombre de archivo no válido'}), 400
    
    if '.' not in foto.filename or foto.filename.rsplit('.', 1)[1].lower() not in extensiones_permitidas:
        return jsonify({'error': 'Extensión de archivo no permitida'}), 400
    
    nombre_unido = str(uuid.uuid4()) + '.' + foto.filename.rsplit('.', 1)[1].lower()
    if not os.path.exists('upload'):
        os.makedirs('upload')
    
    foto.save(os.path.join('upload', nombre_unido))    
    return jsonify({'mensaje': 'Foto subida correctamente', 'nombre_foto': nombre_unido}), 200

# Ruta para ver una foto
@app.route('/foto/<nombre_foto>', methods=['GET'])
def ver_foto(nombre_foto):
    ruta_foto = os.path.join('upload', nombre_foto)
    if not os.path.exists(ruta_foto):
        return jsonify({'error': 'Foto no encontrada'}), 404
    
    return send_file(ruta_foto, mimetype='image/jpeg')

# Ruta para eliminar una foto
@app.route('/eliminar_foto/<nombre_foto>', methods=['DELETE'])
def eliminar_foto(nombre_foto):
    ruta_foto = os.path.join('upload', nombre_foto)
    if not os.path.exists(ruta_foto):
        return jsonify({'error': 'Foto no encontrada'}), 404

    os.remove(ruta_foto)  # Eliminar la foto del sistema de archivos
    return jsonify({'mensaje': 'Foto eliminada correctamente'}), 200

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'interens.contacto@gmail.com'
app.config['MAIL_PASSWORD'] = 'spln pztp ajsr ztqk'  # Contraseña de aplicación de Google

mail = Mail(app)

@app.route('/enviar-correo', methods=['POST'])
def enviar_correo():
    data = request.json
    nombre = data.get('nombre')
    email_usuario = data.get('destinatario')
    mensaje_usuario = data.get('mensaje')

    mensaje = Message(
        sender=f'{email_usuario}',  # Utilizar el correo del usuario como remitente
        subject='Nuevo mensaje de contacto',
        recipients=['interens.contacto@gmail.com'],  # Para (To)
        body=f'Nombre: {nombre}\nCorreo: {email_usuario}\nMensaje: {mensaje_usuario}',
        
    )

    try:
        print(mensaje)
        mail.send(mensaje)
        return jsonify({'mensaje': 'Correo enviado correctamente'}), 200
    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        return jsonify({'error': str(e), 'trace': error_message}), 500
# Otros endpoints y configuración del servidor...


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
# def enviar_correo_restablecimiento(email: str) -> dict:
#     try:
#         response = supabase_client.auth.api.reset_password_for_email(email)
#         if response.status_code == 200:
#             return {"message": "Correo de restablecimiento enviado exitosamente"}
#         else:
#             return {"error": "Error al enviar el correo de restablecimiento"}
#     except Exception as e:
#         return {"error": str(e)}

# def actualizar_contraseña(access_token: str, nueva_contraseña: str) -> dict:
#     try:
#         response = supabase_client.auth.api.update_user(access_token, {"password": nueva_contraseña})
#         if response.status_code == 200:
#             return {"message": "Contraseña actualizada exitosamente"}
#         else:
#             return {"error": "Error al actualizar la contraseña"}
#     except Exception as e:
#         return {"error": str(e)}

# @app.route('/reset-password', methods=['POST'])
# def reset_password():
#     data = request.get_json()
#     token = data['token']
#     new_password = data['new_password']
#     result = actualizar_contraseña(token, new_password)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)