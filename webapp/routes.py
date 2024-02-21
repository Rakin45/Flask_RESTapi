from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from . import db  
from .models import User, WaterQualityData, Location
from .schemas import LocationSchema, UserSchema, UploadedDataSchema, VisualisationDataSchema, WaterQualityDataSchema,WaterQualityUpdateDataSchema
from datetime import datetime
from marshmallow import ValidationError


api_bp = Blueprint('api_bp', __name__)


# Create schema instances
location_schema = LocationSchema()
user_schema = UserSchema()
uploaded_data_schema = UploadedDataSchema()
visualisation_data_schema = VisualisationDataSchema()
water_quality_data_schema = WaterQualityDataSchema()

@api_bp.route('/')
def home():
    # Return the homepage content
    return jsonify({"message": "Welcome to the Water Quality App"}), 200

@api_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify(message="Invalid credentials"), 401

    return jsonify({"message": "Please log in"}), 200

@api_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(message="Signup successful"), 201

    return jsonify({"message": "Signup for a new account"}), 200


@api_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    # Return the user-specific dashboard page content
    return jsonify({"message": "User dashboard"}), 200

@api_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_data():
    # Receive data and return the prediction
    data = request.json.get('data', None)
    # Data will be processed and a prediction will be made
    prediction_result = {"prediction": 0.75}  # Example output
    return jsonify(prediction_result), 201


@api_bp.route('/profile', methods=['GET', 'PATCH'])
@jwt_required()
def user_profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify(message="User not found"), 404

    if request.method == 'GET':
        return user_schema.jsonify(user)

    elif request.method == 'PATCH':
        data = request.get_json()
        
        if 'email' in data:
            user.email = data.get('email')
        if 'password' in data:
            user.set_password(data.get('password'))

        db.session.commit()

        return jsonify(message="Profile updated successfully"), 200

    return jsonify({"message": "User profile page"}), 200


@api_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    # Logic to retrieve the history of user uploads and predictions
    return jsonify({"message": "User history data"}), 200

@api_bp.route('/predictions', methods=['GET'])
@jwt_required()
def get_predictions():
    # Logic to retrieve a list of past predictions with details
    return jsonify({"message": "List of predictions"}), 200

@api_bp.route('/predictions/<prediction_id>', methods=['GET'])
@jwt_required()
def get_prediction(prediction_id):
    # Logic to return the details for a given prediction
    return jsonify({"message": f"Details for prediction {prediction_id}"}), 200


@api_bp.route('/account', methods=['DELETE'])
@jwt_required()
def delete_account():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not user:
        return jsonify(message="User not found"), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify(message="Account deleted successfully"), 202


@api_bp.route('/insights', methods=['GET'])
@jwt_required()
def get_insights():
    # Logic to return insights and trends in water quality data
    return jsonify({"message": "Water quality insights"}), 200

@api_bp.route('/water-quality/<date>/<location_id>', methods=['PUT'])
@jwt_required()
def update_water_quality(date, location_id):
    try:
        date_object = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400
    
    schema = WaterQualityUpdateDataSchema()
    try:
        data = schema.load(request.json)
    except ValidationError as e:
        return jsonify({'error': e.messages}), 400

    # location = Location.query.get(location_id)
    location = db.session.get(Location, location_id)
    print(location)
    if not location:
        return jsonify({'error': "Location not found"}), 404
    
    water_quality_data = WaterQualityData.query.filter_by(
        location_id=location_id, date=date_object).first()

    if not water_quality_data:
        return jsonify({'error': "Water quality record not found"}), 404
    if 'spec_cond_max' in data:
        water_quality_data.spec_cond_max = data['spec_cond_max']
    if 'ph_max' in data:
        water_quality_data.ph_max = data['ph_max']
    if 'ph_min' in data:
        water_quality_data.ph_min = data['ph_min']
    if 'spec_cond_min' in data:
        water_quality_data.spec_cond_min = data['spec_cond_min']
    if 'spec_cond_mean' in data:
        water_quality_data.spec_cond_mean = data['spec_cond_mean']
    if 'dissolved_oxy_max' in data:
        water_quality_data.dissolved_oxy_max = data['dissolved_oxy_max']
    if 'dissolved_oxy_mean' in data:
        water_quality_data.dissolved_oxy_mean = data['dissolved_oxy_mean']
    if 'dissolved_oxy_min' in data:
        water_quality_data.dissolved_oxy_min = data['dissolved_oxy_min']
    if 'temp_mean' in data:
        water_quality_data.temp_mean = data['temp_mean']
    if 'temp_min' in data:
        water_quality_data.temp_min = data['temp_min']
    if 'temp_max' in data:
        water_quality_data.temp_max = data['temp_max']
    if 'water_quality' in data:
        water_quality_data.water_quality = data['water_quality']
    if 'training' in data:
        water_quality_data.training = data['training']
    db.session.commit()
    return jsonify({'message': 'Water quality record updated successfully'}), 200

        

