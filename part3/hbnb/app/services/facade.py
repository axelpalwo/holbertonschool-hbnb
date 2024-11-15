from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

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
        print(f"Usuarios almacenados: {self.user_repo._storage}")
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

    # Creates a Place
    def create_place(self, place_data):
        owner_id = place_data.pop('owner_id')

        # We get all users to verify user id
        user_list = User.get_user_list()
        owner = None
        for user in user_list:
            if user.id == owner_id:
                owner = user
                break

        # We validate owner
        if owner is None:
            raise ValueError(f"User with id {owner_id} not found.")

        # We add 'owner' to dict cause owner_id is not needed anymore
        place_data['owner'] = owner
        new_place = Place(**place_data)
        self.place_repo.add(new_place)
        owner.add_place(new_place)
        return new_place


    # Gets a single Place by ID
    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    # Gets a list of all places
    def get_all_places(self):
        places = self.place_repo.get_all()
        return [
            {
            "id": place.id,
            "title": place.title,
            "latitude": place.latitude,
            "longitude": place.longitude
            }
             for place in places]

    # Updates a Place
    def update_place(self, place_id, place_data):
        return self.place_repo.update(place_id, place_data)

    # Deletes a Place
    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)

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
    
    # Creates a review
    def create_review(self, review_data):
        # We get user and place id related to the review
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')

        # Verify if User and Place exists
        user_list = User.get_user_list()
        r_user = None
        for user in user_list:
            if user.id == user_id:
                r_user = user
                break
        places_list = Place.get_places()
        r_place = None
        for place in places_list:
            if place.id == place_id:
                r_place = place
                break
        # If doesn't exist raises ValueError
        if r_user is None or r_place is None:
            raise ValueError(f"User with id {user_id} or Place with id {place_id} not found")

        # Preparing review package for instance initialization
        review_data['user'] = r_user
        review_data['place'] = r_place
        new_review = Review(**review_data)
        r_place.add_review(new_review)
        self.review_repo.add(new_review)
        return new_review

    # Gets a Review by ID
    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    # Gets all Reviews
    def get_all_reviews(self):
        reviews = self.review_repo.get_all()
        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating
            }
             for review in reviews]

    # Gets Reviews by Place Attribute
    def get_reviews_by_place(self, place_id):
        review_list = Review.get_review_list()
        return [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating
            }
             for review in review_list if review.place.id == place_id]

    # Updates a Review
    def update_review(self, review_id, review_data):
        return self.review_repo.update(review_id, review_data)

    # Deletes a Review
    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
    
facade = HBnBFacade()