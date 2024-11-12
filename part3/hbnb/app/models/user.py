from . import BaseModel
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(BaseModel):

    __users__ = []

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        if super().str_validate("first_name", first_name) and super().str_validate("last_name", last_name):
            if len(first_name) > 50 and len(last_name) > 50:
                raise ValueError("Maximum length of 50 characters.")
        if super().email_validate(email):
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
        if super().str_validate('password', password):
            self.hash_password(password)
        self.is_admin = is_admin
        self.places = []
        User.__users__.append(self) #Añade el nuevo usuario a la lista de Usuarios
    
    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # Modifica los datos de un usuario
    def update(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        if super().str_validate("first_name", first_name) and super().str_validate("last_name", last_name):
            if len(first_name) > 50 and len(last_name) > 50:
                raise ValueError("Maximum length of 50 characters.")
        if super().email_validate(email):
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
            super().save()
            return True
        return False

    #Agrega el/los lugares en que el User es Owner
    def add_place(self, place):
        self.places.append(place)

    def to_dict(self):
        """Convert the User object into a dictionary format."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

    #Devuelve lista de usuarios
    @staticmethod
    def get_user_list():
        return User.__users__