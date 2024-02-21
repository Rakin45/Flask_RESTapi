from webapp import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False,unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=True)
    company = db.Column(db.String, nullable=True)
    profession = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Location(db.Model):
    __tablename__ = 'locations'

    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    water_quality_data = db.relationship('WaterQualityData', back_populates='location')

    def __repr__(self):
        return f'<Location {self.location_name}>'



class UploadedData(db.Model):
    __tablename__ = 'uploaded_data'

    data_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    data = db.Column(db.String, nullable=False)

    user = db.relationship('User', backref='uploaded_data')
    location = db.relationship('Location', backref='uploaded_data')

    def __repr__(self):
        return f'<UploadedData {self.data_id}>'

class VisualisationData(db.Model):
    __tablename__ = 'visualisation_data'

    visualisation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    upload_id = db.Column(db.Integer, db.ForeignKey('uploaded_data.data_id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    forecast_data = db.Column(db.String, nullable=True)

    upload = db.relationship('UploadedData', back_populates='visualisation_data')
    location = db.relationship('Location', back_populates='visualisation_data')

class WaterQualityData(db.Model):
    __tablename__ = 'water_quality_data'

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)

    spec_cond_max = db.Column(db.Float, nullable=True)
    ph_max = db.Column(db.Float, nullable=True)
    ph_min = db.Column(db.Float, nullable=True)
    spec_cond_min = db.Column(db.Float, nullable=True)
    spec_cond_mean = db.Column(db.Float, nullable=True)
    dissolved_oxy_max = db.Column(db.Float, nullable=True)
    dissolved_oxy_mean = db.Column(db.Float, nullable=True)
    dissolved_oxy_min = db.Column(db.Float, nullable=True)
    temp_mean = db.Column(db.Float, nullable=True)
    temp_min = db.Column(db.Float, nullable=True)
    temp_max = db.Column(db.Float, nullable=True)
    water_quality = db.Column(db.Float, nullable=True)
    training = db.Column(db.Boolean, nullable=True)

    location = db.relationship('Location', back_populates='water_quality_data')

    def __repr__(self):
        return f'<WaterQualityData id={self.id}, Location ID={self.location_id}, Date={self.date}>'

# Back populates defined outside of classes to avoid circular import issues
UploadedData.visualisation_data = db.relationship('VisualisationData', uselist=False, back_populates='upload')
Location.visualisation_data = db.relationship('VisualisationData', back_populates='location')