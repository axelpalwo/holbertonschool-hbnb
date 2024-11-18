from app import db
from sqlalchemy import Column, Integer, String
from app.models.baseclass import BaseModel

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    def __init__(self, name):
        # String validator
        if not isinstance(name, str):
            raise TypeError("Invalid input data")
        elif name == '':
            raise ValueError("Invalid input data")
        # Length validator
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
        self.name = name

    def update(self, name):
        """Updates Amenity's name"""
        # String validator
        if not isinstance(name, str):
            raise TypeError("Invalid input data")
        elif name == '':
            raise ValueError("Invalid input data")
        # Length validator
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
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
