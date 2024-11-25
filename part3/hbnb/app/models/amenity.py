from app import db
from sqlalchemy import Column, Integer, String
from app.models.baseclass import BaseModel
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    
    def update(self, name):
        """Updates Amenity's name"""
        self.name = name
        db.session.commit()
        return True

    def to_dict(self):
        """Converts Amenity in Dic"""
        return {
            'id': self.id,
            'name': self.name,
        }

    @staticmethod
    def get_amenities():
        """Gets all Amenitys from query"""
        return Amenity.query.all()

    @validates('name')
    def validate_name(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Invalid input data")
        if len(value) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
        return value