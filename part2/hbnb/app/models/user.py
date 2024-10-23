from . import BaseModel

class User(BaseModel):

    __users__ = []

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if super().str_validate("first_name", first_name) and super().str_validate("last_name", last_name):
            if len(first_name) > 50 and len(last_name) > 50:
                raise ValueError("Maximum length of 50 characters.")
        if super().str_validate("email", email):
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
        self.is_admin = is_admin
        self.places = []
        User.__users__.append(self) #Añade el nuevo usuario a la lista de Usuarios
        
    # Modifica los datos de un usuario
    def update(self, id, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        if super().str_validate("first_name", first_name) and super().str_validate("last_name", last_name):
            if len(first_name) > 50 and len(last_name) > 50:
                raise ValueError("Maximum length of 50 characters.")
        if super().str_validate("email", email):
            user_list = User.get_user_list()
            for user in user_list:
                if user.id == id:
                    self.first_name = first_name
                    self.last_name = last_name
                    self.email = email
                    super().save()
                    return True
        return False
    # Delete pendiente, buscar otro metodo
    def delete(self, id):
        user_to_delete = None
        for user in User.__users__:
            if user.id == id:
                user_to_delete = user
                break
        
        if user_to_delete:
            User.__users__.remove(user_to_delete)
            return {
                'first_name': user_to_delete.first_name,
                'last_name': user_to_delete.last_name,
                'email': user_to_delete.email
            }
        else:
            raise ValueError(f"User with id {id} not found.")

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
        return [user.to_dict() for user in User.__users__]
