from typing import List
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from webapp import db

class Location(db.Model):
    __tablename__ = 'locations'
    
    location_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    location_name: Mapped[str] = mapped_column(db.Text, nullable=False)
    latitude: Mapped[float] = mapped_column(db.Float, nullable=True)
    longitude: Mapped[float] = mapped_column(db.Float, nullable=True)
    
    def __repr__(self):
        return f'<Location {self.location_name}>'




class User(db.Model):
    user_id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.Text, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.Text, unique=False, nullable=False)
    full_name: Mapped[str] = mapped_column(db.Text, unique=False, nullable=True)
    company: Mapped[str] = mapped_column(db.Text, unique=False, nullable=True)
    profession: Mapped[str] = mapped_column(db.Text, unique=False, nullable=True)


    def __init__(self, email: str, password: str, full_name: str, company: str, profession: str):
        """
        Create a new User object using hashing the plain text password.
        :type password_string: str
        :type email: str
        :returns None
        """
        self.email = email
        self.password = password
        self.full_name = full_name
        self.company = company
        self.profession = profession