from app import db
from sqlalchemy.orm import relationship, joinedload, validates
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.baseclass import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False)
    place_id = Column(String, ForeignKey('places.id'), nullable=False)

    user = relationship('User', back_populates='reviews')
    place = relationship('Place', back_populates='reviews')

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def update(self, data):
        """Updates Review's data"""
        text = data.get('text')
        rating = data.get('rating')
        self.text = text
        self.rating = rating
        db.session.commit()
        return True

    def to_dict(self):
        """Converts Review in a Dic"""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id
        }

    @staticmethod
    def get_reviews():
        """Gets a list of all Review's"""
        return Review.query.options(joinedload(Review.place)).all()

    @validates('text')
    def validate_name(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Invalid input data")
        return value
    
    @validates('rating')
    def validate_rating(self, key, value):
        if isinstance(value, int):
            if value < 1 and value > 5:
                raise ValueError("Invalid input data")
        else:
            raise TypeError("Invalid input data")
        return value
