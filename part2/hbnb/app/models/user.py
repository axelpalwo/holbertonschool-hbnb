from . import BaseModel

class User(BaseModel):

    __users__ = []

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []
        User.__users__.append(self)

    def register(self, first_name, email, password):
        return self.id

    def update(self, first_name, last_name, email, password):
        return True
    
    def delete(self, id):
        return True
    
    def add_place(self, place):
        self.places.append(place)

    def get_user_list():
        return User.__users__