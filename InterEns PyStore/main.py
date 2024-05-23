from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid 
import requests
import json
# import supabase

app = Flask(__name__)
CORS(app)

URL_SUPEBASE = 'https://gglsaoykhjniypthjgfc.supabase.co/rest/v1/'
supebaseheads = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbHNhb3lraGpuaXlwdGhqZ2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ1NTIwMTQsImV4cCI6MjAzMDEyODAxNH0.jmngoEfB87raLwTHDq1DI347a4owyHCqs75VSJUwMZo'
# os.environ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbHNhb3lraGpuaXlwdGhqZ2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ1NTIwMTQsImV4cCI6MjAzMDEyODAxNH0.jmngoEfB87raLwTHDq1DI347a4owyHCqs75VSJUwMZo'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbHNhb3lraGpuaXlwdGhqZ2ZjIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxNDU1MjAxNCwiZXhwIjoyMDMwMTI4MDE0fQ.FTBFPMMnJOACE2iYWt47XaTF8_wjD0anXfyrVEPV74k'
# supabase_anon_key = os.getenv('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdnbHNhb3lraGpuaXlwdGhqZ2ZjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ1NTIwMTQsImV4cCI6MjAzMDEyODAxNH0.jmngoEfB87raLwTHDq1DI347a4owyHCqs75VSJUwMZo')

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



# Obtener todos los productos de Supabase
@app.route('/obtener_productos', methods=['GET'])
def obtener_productos():
    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'PRODUCTO?select=*', headers=headers)
    return response.json(), response.status_code

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
    id_producto = request.args.get('id_producto')
    headers = {'apikey': supebaseheads}
    response = requests.get(URL_SUPEBASE + 'IMAGEN_PRODUCTO?id_producto=eq.' + id_producto, headers=headers)
    if response.status_code == 200:
        return response.json(), response.status_code
    else:
        return jsonify({'error': 'Error en el servidor'}), 500


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


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