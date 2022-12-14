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

@app.route('/members', methods=['GET'])
def get_all_members():
    status = 200
    # this is how you can use the Family datastructure by calling its methods
    try:
        members = jackson_family.get_all_members()
        response_body = members
    except:
        response_body = {
            "msg": "El servidor esta en las ultimas :-("
        }
        status = 500

    return jsonify(response_body), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    status = 200
    try:
        member = jackson_family.get_member(id)
        response_body = member
    except:
        response_body = {
            "msg": "El servidor esta en las ultimas :-("
        }
        status = 500

    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    status = 200 
    body = request.json
    if body is None:
        response_body = {
            "msg": "El cuerpo esta vacio "
        }
        status = 400
    else:
        try:
            member = jackson_family.add_member(body)
            response_body = member
        except:
            response_body = {
            "msg": "El servidor exploto :-o"
            }
            status = 500

    return jsonify(response_body), status

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    status = 200
    try:
        member = jackson_family.delete_member(id)
        if member == False:
            response_body = {
                "msg": "No se encuentra esa persona"
            }
            status = 404
        else:
            response_body = {
                "done": True
            }
    except:
            response_body = {
            "msg": "El servidor se cayo :'-("
            }
            status = 500
    return jsonify(response_body), status

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)