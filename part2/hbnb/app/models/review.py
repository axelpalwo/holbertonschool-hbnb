from . import BaseModel

class Review(BaseModel):

    review_list = []

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place #Obj Place
        self.user = user #Obj User
        Review.review_list.append(self)

    def create(self, place, user, rating, comment):
        return id
    
    def update(self, id, rating, comment):
        return True
    
    def delete(self, id):
        return True
    
    def get_review_list():
        return Review.review_list