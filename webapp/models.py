from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp import db

class Location(db.Model):
    __tablename__ = 'locations'
    
    location_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    location_name: Mapped[str] = mapped_column(db.String, nullable=False)
    latitude: Mapped[float] = mapped_column(db.Float, nullable=True)
    longitude: Mapped[float] = mapped_column(db.Float, nullable=True)
    water_quality_data: Mapped[List['WaterQualityData']] = relationship('WaterQualityData', back_populates='location')
    def __repr__(self):
        return f'<Location {self.location_name}>'

class User(db.Model):
    __tablename__ = 'users'
    
    user_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String, nullable=False)
    full_name: Mapped[str] = mapped_column(db.String, nullable=True)
    company: Mapped[str] = mapped_column(db.String, nullable=True)
    profession: Mapped[str] = mapped_column(db.String, nullable=True)
    
    

class UploadedData(db.Model):
    __tablename__ = 'uploaded_data'
    
    data_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    location_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    data: Mapped[str] = mapped_column(db.String, nullable=False)
    
    # Define relationships with 'backref' and 'back_populates'
    user: Mapped[User] = relationship('User', backref='uploaded_data')
    location: Mapped[Location] = relationship('Location', backref='uploaded_data')
    
    def __repr__(self):
        return f'<UploadedData {self.data_id}>'

class VisualisationData(db.Model):
    __tablename__ = 'visualisation_data'
    
    visualisation_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    upload_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('uploaded_data.data_id'), nullable=False)
    location_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    forecast_data: Mapped[str] = mapped_column(db.String, nullable=True)
    
    # Relationships must correspond with those defined in UploadedData and Location
    upload: Mapped[UploadedData] = relationship('UploadedData', back_populates='visualisation_data')
    location: Mapped[Location] = relationship('Location', back_populates='visualisation_data')

class WaterQualityData(db.Model):
    __tablename__ = 'water_quality_data'
    
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    location_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    date: Mapped[date] = mapped_column(db.Date, nullable=False)
    
    spec_cond_max: Mapped[float] = mapped_column(db.Float, nullable=True)
    ph_max: Mapped[float] = mapped_column(db.Float, nullable=True)
    ph_min: Mapped[float] = mapped_column(db.Float, nullable=True)
    spec_cond_min: Mapped[float] = mapped_column(db.Float, nullable=True)
    spec_cond_mean: Mapped[float] = mapped_column(db.Float, nullable=True)
    dissolved_oxy_max: Mapped[float] = mapped_column(db.Float, nullable=True)
    dissolved_oxy_mean: Mapped[float] = mapped_column(db.Float, nullable=True)
    dissolved_oxy_min: Mapped[float] = mapped_column(db.Float, nullable=True)
    temp_mean: Mapped[float] = mapped_column(db.Float, nullable=True)
    temp_min: Mapped[float] = mapped_column(db.Float, nullable=True)
    temp_max: Mapped[float] = mapped_column(db.Float, nullable=True)
    water_quality: Mapped[str] = mapped_column(db.Float, nullable=True)
    
    # Relationship to Location
    location: Mapped['Location'] = relationship('Location', back_populates='water_quality_data')

    def __repr__(self):
        return (f'<WaterQualityData id={self.id}, '
                f'Location ID={self.location_id}, Date={self.date}>')

# Back populates defined outside of classes to avoid circular import issues
UploadedData.visualisation_data = relationship('VisualisationData', uselist=False, back_populates='upload')
Location.visualisation_data = relationship('VisualisationData', back_populates='location')