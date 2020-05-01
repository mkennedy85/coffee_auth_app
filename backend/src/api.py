import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()

## ROUTES
@app.route('/drinks')
def get_drinks_short():
    selection = Drink.query.all()
    drinks = list(map(Drink.short, selection))

    result = {
        "success": True,
        "drinks": drinks
    }
    return jsonify(result)

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_long(jwt):
    selection = Drink.query.all()
    drinks = list(map(Drink.long, selection))

    result = {
        "success": True,
        "drinks": drinks
    }
    return jsonify(result)

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(jwt):
    try:
        title = request.get_json()["title"]
        recipe = request.get_json()['recipe']
        data = {
            "title": title,
            "recipe": json.dumps(recipe),
        }  
        drink = Drink(**data)
        drink.insert()
    except:
        abort(422)

    result = {
        "success": True,
        "drinks": data
    }
    return jsonify(result)

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(jwt, id):
    try:
        selection = Drink.query.filter(Drink.id == id).first()
        if "title" in request.get_json() : selection.title = request.get_json()["title"]
        if "recipe" in request.get_json() : selection.recipe = json.dumps(request.get_json()["recipe"])
        selection.update()
    except:
        abort(404)

    result = {
        "success": True,
        "drinks": [selection.long()]
    }
    return jsonify(result)

@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(jwt, id):
    try:
        selection = Drink.query.get(id)
        selection.delete()
    except:
        abort(404)

    result = {
        "success": True,
        "delete": int(id)
    }
    return jsonify(result)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False,
                    "error": 404,
                    "message": 'Not Found'
                    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "Unprocessable Entity"
                    }), 422

@app.errorhandler(AuthError)
def auth_error(ex):
    return jsonify({
                    "success": False,
                    "error": ex.status_code,
                    "code": ex.error["code"],
                    "description": ex.error["description"]
                    }), ex.status_code
