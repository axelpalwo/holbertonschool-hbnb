from app import db
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship, validates
from app.models.baseclass import BaseModel

# Intermediate Table for Places-Amenities
place_amenity = db.Table('place_amenities',
    Column('place_id', String, ForeignKey('places.id'), primary_key=True),
    Column('amenity_id', String, ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    owner_id = Column(String, ForeignKey('users.id'), nullable=False)
    
    owner = relationship('User', back_populates='places')
    reviews = relationship('Review', back_populates='place', cascade="all, delete-orphan")
    amenities = relationship('Amenity', secondary=place_amenity, backref='places')

    def __init__(self, title, description, price, latitude, longitude, owner, amenities=None):
        super().__init__()
        self.title = title
        # If there is a description
        if description:
            self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.amenities = amenities or []

    def update(self, data):
        """Updates place's data"""
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        self.title = title
        self.description = description
        self.price = price
        db.session.commit()
        return True

    def delete(self):
        """Deletes the Place"""
        db.session.delete(self)
        db.session.commit()

    def add_amenity(self, amenity_id):
        """ Adds an Amenity to the Place """
        if amenity_id not in self.amenities_ids:
            self.amenities_ids.append(amenity_id)

    def to_dict(self):
        """Converts the Place in a Dic"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id,
            'amenities': self.amenities_ids
        }

    @staticmethod
    def get_places():
        """Gets a list from all Places"""
        return Place.query.all()

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Invalid input data")
        if value < -180 or value > 180:
            raise ValueError("Invalid input data")
        return value
    
    @validates('latitude')
    def validate_latitude(self, key, value):
        if not isinstance(value, float):
            raise TypeError("Invalid input data")
        if value < -90 or value > 90:
            raise ValueError("Invalid input data")
        return value
    
    @validates('price')
    def validate_price(self, key, value):
        if not isinstance(value, float) or value < 0:
            raise ValueError("Price must be a positive number.")
        return value
    
    @validates('title')
    def validate_title(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Invalid input data")
        if len(value) > 100:
            raise ValueError("Maximum length of 100 characters.")
        return value
    