from webapp.models import User,WaterQualityData, Location
from webapp import db
import json
from datetime import datetime

def add_test_user(client):
    test_user = User(username='newuser', email='new@example.com', password='password123')
    db.session.add(test_user)
    db.session.commit()


def login(client, username, password):
    response = client.post('/login', json={"username": username, "password": password})
    print(response)
    return response.json.get('access_token', None)

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the Water Quality App"}

def test_signup(client):
    response = client.post('/signup', json={"username": "newuser", "email": "new@example.com", "password": "password123"})
    assert response.status_code == 201
    assert response.json == {"message": "Signup successful"}

def test_login_endpoint(client):
    add_test_user(client)

    # Test valid login
    response = client.post('/login', json={"username": "newuser", "password": "password123"})
    assert response.status_code == 200
    assert 'access_token' in response.json
    
def test_login_endpoint_invalid(client):
    # Test invalid login
    response = client.post('/login', json={"username": "invalid_user", "password": "invalid_password"})
    assert response.status_code == 401
    assert response.json == {"message": "Invalid credentials"}

def test_login_and_dashboard(client):
    add_test_user(client)
    access_token = login(client, "newuser", "password123")
    assert access_token is not None

    response = client.get('/dashboard', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json == {"message": "User dashboard"}

def test_upload_and_predictions(client):
    add_test_user(client)
    access_token = login(client, "newuser", "password123")
    assert access_token is not None

    data = {"data": {"feature1": 1, "feature2": 2}}
    response_upload = client.post('/upload', json=data, headers={"Authorization": f"Bearer {access_token}"})
    assert response_upload.status_code == 201
    assert response_upload.json == {"prediction": 0.75}

def test_profile(client):
    add_test_user(client)
    access_token = login(client, "newuser", "password123")
    assert access_token is not None

    response_get_profile = client.get('/profile', headers={"Authorization": f"Bearer {access_token}"})
    assert response_get_profile.status_code == 200
    assert "new@example.com" in str(response_get_profile.data)

    data = {"email": "newemail@example.com", "password": "newpassword"}
    response_update_profile = client.patch('/profile', json=data, headers={"Authorization": f"Bearer {access_token}"})
    assert response_update_profile.status_code == 200
    assert "Profile updated successfully" in str(response_update_profile.data)

def test_dashboard_endpoint(client):
    add_test_user(client)
    token = login(client, 'newuser', 'password123')
    response = client.get('/dashboard', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json == {"message": "User dashboard"}
    

def test_insights_endpoint(client):
    add_test_user(client)
    token = login(client, 'newuser', 'password123')
    response = client.get('/insights', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json == {"message": "Water quality insights"}


def test_delete_account(client):
    add_test_user(client)
    access_token = login(client, "newuser", "password123")
    assert access_token is not None

    response_delete_account = client.delete('/account', headers={"Authorization": f"Bearer {access_token}"})
    assert response_delete_account.status_code == 202
    assert "Account deleted successfully" in str(response_delete_account.data)

def test_upload_endpoint(client):
    add_test_user(client)
    token = login(client, 'newuser', 'password123')
    response = client.post('/upload', json={"data": {"parameter": "value"}}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert 'prediction' in response.json


def test_update_water_quality_endpoint(client):
    # Set up test data
    location = Location(location_name='Test Location', latitude=0.0, longitude=0.0)
    db.session.add(location)
    db.session.commit()

    valid_date = '2022-02-21'
    invalid_date = 'invalid-date'

    valid_data = {
        "spec_cond_max": 1.23,
        "ph_max": 7.5,
        # Include other fields as needed
    }

    # Create a test water quality record
    water_quality_record = WaterQualityData(
        location=location,
        date=datetime.strptime(valid_date, '%Y-%m-%d').date(),
        spec_cond_max=0.0,
    )
    db.session.add(water_quality_record)
    db.session.commit()

    add_test_user(client)
    
    access_token = login(client, "newuser", "password123")
    
    # Test with valid date and data
    response = client.put(f'/water-quality/{valid_date}/{location.location_id}',
                          data=json.dumps(valid_data),
                          content_type='application/json',
                          headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    assert response.json == {'message': 'Water quality record updated successfully'}

    # Test with invalid date format
    response_invalid_date = client.put(f'/water-quality/{invalid_date}/{location.location_id}',
                                       data=json.dumps(valid_data),
                                       content_type='application/json',
                                       headers={'Authorization': f'Bearer {access_token}'})

    assert response_invalid_date.status_code == 400
    assert response_invalid_date.json == {'error': 'Invalid date format. Use YYYY-MM-DD.'}

    # Test with non-existing location
    response_not_found_location = client.put(f'/water-quality/{valid_date}/999',
                                            data=json.dumps(valid_data),
                                            content_type='application/json',
                                            headers={'Authorization': f'Bearer {access_token}'})

    assert response_not_found_location.status_code == 404
    assert response_not_found_location.json == {'error': 'Location not found'}

    # Test with non-existing water quality record
    response_not_found_record = client.put(f'/water-quality/2022-02-22/{location.location_id}',
                                          data=json.dumps(valid_data),
                                          content_type='application/json',
                                          headers={'Authorization': f'Bearer {access_token}'})
    
    assert response_not_found_record.status_code == 404
    assert response_not_found_record.json == {'error': 'Water quality record not found'}

    # Clean up test data

    Location.query.filter_by(location_name='Test Location').delete()
    WaterQualityData.query.filter_by(location=location).delete()
    db.session.commit()


# Test for the '/history' endpoint
def test_get_history_endpoint(client):
    add_test_user(client)
    access_token = login(client, "newuser", "password123")

    response = client.get('/history', headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == 200
    assert response.json == {"message": "User history data"}

# Test for the '/predictions' endpoint
def test_get_predictions_endpoint(client):
    add_test_user(client)
    access_token = login(client, "newuser", "password123")
    
    response = client.get('/predictions', headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == 200
    assert response.json == {"message": "List of predictions"}

# Test for the '/predictions/<prediction_id>' endpoint
def test_get_prediction_endpoint(client):
    add_test_user(client)
    access_token = login(client, "newuser", "password123")
    
    prediction_id = 123  # Replace with a valid prediction ID
    response = client.get(f'/predictions/{prediction_id}', headers={'Authorization': f'Bearer {access_token}'})
    
    assert response.status_code == 200
    assert response.json == {"message": f"Details for prediction {prediction_id}"}