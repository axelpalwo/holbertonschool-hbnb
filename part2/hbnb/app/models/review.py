from . import BaseModel

class Review(BaseModel):

    review_list = []

    def __init__(self, text, rating, place, user):
        super().__init__()
        if super().str_validate("review text", text):
            self.text = text
        if super().rating_validate(rating):
            self.rating = rating
        if super().validate_place(place):
            self.place = place
        if super().validate_user(user):
            self.user = user
        Review.review_list.append(self) #Agrega una Review al crearse a la lista de clase

    def update(self, id, rating, comment):
        if super().str_validate("comment", comment):
            review_list = Review.get_review_list()
            for review in review_list:
                if review.id == id:
                    review.rating = rating
                    review.comment = comment
                    return True
        return False
    
    def delete(self, id):
        return True
    
    #Devuelve una lista de todas las Reviews
    def get_review_list():
        return Review.review_list