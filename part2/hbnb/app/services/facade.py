from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        new_user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'])
        self.user_repo.add(new_user)
        return new_user

    def get_user(self, id):
        return self.user_repo.get(id)

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)