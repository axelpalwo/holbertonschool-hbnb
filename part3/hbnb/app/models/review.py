from app import db
from sqlalchemy.orm import relationship, joinedload
from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.baseclass import BaseModel

class Review(BaseModel):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    place_id = Column(Integer, ForeignKey('places.id'), nullable=False)

    user = relationship('User', back_populates='reviews')
    place = relationship('Place', back_populates='reviews')

    def __init__(self, text, rating, place, user):
        # String validator
        if not isinstance(text, str):
            raise TypeError("Invalid input data")
        elif text == '':
            raise ValueError("Invalid input data")
        else:
            self.text = text
        # Number validator
        if isinstance(rating, int):
            if rating < 1 or rating > 5:
                raise ValueError("Invalid input data")
        else:
            raise TypeError("Invalid input data")
        self.rating = rating
        self.place = place
        self.user = user

    def update(self, data):
        """Updates Review's data"""
        text = data.get('text')
        rating = data.get('rating')
        # String validator
        if not isinstance(text, str):
            raise TypeError("Invalid input data")
        elif text == '':
            raise ValueError("Invalid input data")
        else:
            self.text = text
        # Number validator
        if isinstance(rating, int):
            if rating < 1 or rating > 5:
                raise ValueError("Invalid input data")
        else:
            raise TypeError("Invalid input data")
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
