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
                    review.text = comment
                    super().save()
                    return True
        return False
    
    def delete(self, id):
        review_to_delete = None
        for review in Review.review_list:
            if review.id == id:
                review_to_delete = review
                break;
        if review_to_delete:
            Review.review_list.remove(review_to_delete)
            return { 'user': review_to_delete.user,
                     'place': review_to_delete.place,
                     'rating': review_to_delete.rating,
                     'text': review_to_delete.text
                     }
        else:
            raise ValueError(f"Review with id {id} not found.")
    
    #Devuelve una lista de todas las Reviews
    def get_review_list():
        return Review.review_list