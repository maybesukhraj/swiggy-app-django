import os
import sys
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

# --- Path Fix ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_delivery.settings')

import django
django.setup()

from restaurantmgmt.models import Restaurant
from django.contrib.auth import authenticate

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'fallback-secret')
jwt = JWTManager(app)

@app.route('/api/v1/token/', methods=['POST'])
def get_token():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid credentials"}), 401

@app.route('/api/v1/restaurants/', methods=['GET'])
@jwt_required()
def list_restaurants():
    restaurants = Restaurant.objects.all().values('id', 'name', 'location')
    return jsonify(list(restaurants)), 200

if __name__ == "__main__":
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(rule)
    app.run(debug=True, host="0.0.0.0", port=5000)

