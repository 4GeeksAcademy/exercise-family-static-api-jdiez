"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



Michael = {
    "first_name": "Michael",
    "age" : 30,
    "lucky_numbers": [2,4,8]
}

John = {
    "first_name": "John",
    "age" : 20,
    "lucky_numbers": [12,44,58]
}

Peter = {
    "first_name": "Peter",
    "age" : 25,
    "lucky_numbers": [10,20,30]
}

jackson_family.add_member(Michael)
jackson_family.add_member(John)
jackson_family.add_member(Peter)


@app.route('/members', methods=['POST'])
def new_member():
    new_member = request.json
    member = jackson_family.add_member(new_member)
    if(member):
        return jsonify({"Mensaje": "Se añadió el miembro con éxito"}), 200
    return jsonify({"Mensaje": "Error al añadir el miembro"}), 400

@app.route('/members/<int:id>', methods=['GET'])
def get_one_member(id):
    member = jackson_family.get_member(id)
    response_body = {
        "Miembro seleccionado": member
    }
    return jsonify(response_body), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    member = jackson_family.delete_member(id)
    response_body = {
        "Miembro eliminado": member
    }
    return jsonify(response_body), 200

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
