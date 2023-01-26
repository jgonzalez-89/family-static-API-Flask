import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import Family

# Creación de una instancia de la aplicación Flask
app = Flask(__name__)
# Deshabilitar el uso de barras diagonales en las URLs
app.url_map.strict_slashes = False
# Habilitar CORS para permitir solicitudes desde orígenes externos
CORS(app)

# Creación de una instancia de la clase Family
family = Family("Jackson")

# Manejador de errores personalizado para las excepciones de la clase APIException
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Ruta para generar el mapa del sitio
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Ruta para obtener todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_all_members():
    return jsonify(family.get_all_members() if family.get_all_members()
                   != None else {"message": "Not Found"}), 200 if family.get_all_members() != None else 400

# Ruta para obtener un miembros específico de la familia por su id
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member_by_id(member_id):
    member = family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"message": "Not Found"}), 400

# Ruta para agregar un nuevo miembro a la familia
@app.route('/member', methods=['POST'])
def add_member():
    request_body = request.json
    member = {'id': request_body.get('id') or family._generateId(),
              'first_name': request_body.get('first_name'),
              'age': request_body.get('age'),
              'lucky_numbers': request_body.get('lucky_numbers')}
    if not all(member.values()):
        return jsonify({"message": "Not Found"}), 400

    response_body = family.add_member(member)
    return jsonify(response_body), 200

# Ruta para eliminar un miembro especifico de la familia por su id
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    response_body = {"done": family.delete_member(member_id)}
    return jsonify(response_body), 200 if response_body["done"] else (jsonify({"message": "Not Found"}), 400)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
