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
    def update(self, id, first_name, last_name, email):
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
                    return True
        return False
    # Delete pendiente, buscar otro metodo
    def delete(self, id):
        user_list = self.__users__
        new_user_list = []
        for user in user_list:
            if user.id != id:
                new_user_list.append(user)
            else:
                deleted_user = user
        self.__users__ = new_user_list
        return {'first_name': deleted_user.first_name,
                'last_name': deleted_user.last_name,
                'email': deleted_user.email
                }
    #Agrega el/los lugares en que el User es Owner
    def add_place(self, place):
        self.places.append(place)

    #Devuelve lista de usuarios
    def get_user_list():
        return User.__users__