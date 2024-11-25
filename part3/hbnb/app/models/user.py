from app import db, Bcrypt
from sqlalchemy.orm import relationship, validates
from sqlalchemy import Column, String, Boolean
from app.models.baseclass import BaseModel
from validate_email_address import validate_email

bcrypt = Bcrypt()

class User(BaseModel):
    __tablename__ = 'users'

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    is_admin = Column(Boolean, default=False)

    places = relationship("Place", back_populates="owner", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.hash_password(password)

    
    def hash_password(self, password):
        """Hashes password"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Compares hashed passwords"""
        return bcrypt.check_password_hash(self.password, password)

    # def update(self, data):
    #     """Updates User data"""
    #     first_name = data.get('first_name')
    #     last_name = data.get('last_name')
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     db.session.commit()

    def add_place(self, place):
        """Adds a Place to an User"""
        self.places.append(place)

    def to_dict(self):
        """Converts User in a Dic"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

    @staticmethod
    def get_user_list():
        """Gets a list of all Users"""
        return User.query.all()

    @validates('first_name', 'last_name')
    def validate_name(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Invalid input data")
        if len(value) > 50:
            raise ValueError("Maximum length of 50 characters.")
        return value
    
    @validates('email')
    def validate_email(self, key, value):
        if not validate_email(value):
            raise ValueError("Invalid input data")
        return value