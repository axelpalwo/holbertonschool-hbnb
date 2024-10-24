from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    
    # =============================== [ USER METHODS ] ===============================
    # Creates an User
    def create_user(self, user_data):
        new_user = User(**user_data)
        self.user_repo.add(new_user)
        return new_user
    
    # Gets a single User by ID
    def get_user(self, id):
        return self.user_repo.get(id)

    # Gets all Users
    def get_users_list(self):
        users = self.user_repo.get_all()
        return [user.to_dict() for user in users]
    
    # Updates an User
    def update_user(self, id, data):
        return self.user_repo.update(id, data)

    # Deletes an User
    def delete_user(self, id):
        return self.user_repo.delete(id)

    # Gets an User by Email
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)
    
    # Adds a Place to an Owner
    def add_user_place(self, id_user, id_place):
        user = self.get_user(id_user)
        if user:
            place = self.get_place(id_place)
            if place:
                user.add_place(place)
                return user
    
    # =============================== [ PLACE METHODS ] ===============================

    # Creates a new Place
    def create_place(self, place_data):
        new_place = Place(**place_data)
        self.place_repo.add(new_place)
        return new_place

    # Gets a single Place by ID
    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        places = self.place_repo.get_all()
        return [place.to_dict() for place in places]

    # Updates a Place
    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    # Deletes a Place
    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

    # Add Review to a Place

    # Add Amenity to a Place


    # =============================== [ AMENITIES METHODS ] ===============================

    # Creates an Amenity
    def create_amenity(self, amenity_data):
        amenity_name = amenity_data.get('name')
        new_amenity = Amenity(amenity_name)
        self.amenity_repo.add(new_amenity)
        return new_amenity

    # Gets an Amenity by ID
    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    # Gets all Amenities
    def get_all_amenities(self):
        amenities = self.amenity_repo.get_all()
        return [amenity.to_dict() for amenity in amenities]

    # Updates an Amenity by ID
    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update(amenity_id, amenity_data)
    
    # Deletes an Amenity
    def delete_amenity(self, id):
        return self.amenity_repo.delete(id)
    
    # =============================== [ REVIEWS METHODS ] ===============================