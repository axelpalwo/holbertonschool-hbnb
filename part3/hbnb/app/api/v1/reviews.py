from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'You cannot review your own place')
    @api.response(400, 'You have already reviewed this place')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        """Register a new review"""
        data = api.payload

        # Get Place data from place_id
        place_data = facade.get_place(data.get('place_id'))

        # Check Owner_id with User review's id
        if current_user['id'] == place_data.owner.id:
            return {'error': 'You cannot review your own place.'}, 400
        
        # Check if User has a previous review
        for user_review in place_data.reviews:
            if user_review.user.id == current_user['id']:
                return {'error': 'You have already reviewed this place.'}, 400
        try:
            new_review = facade.create_review(data)
            return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": new_review.user.id,
                "place_id": new_review.place.id,

                }, 201
        except TypeError as e:
            return {'error': str(e)}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(404, 'No reviews found')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        if not reviews:
            return { 'error': 'No reviews found' }, 404
        return reviews, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)

        if not review:
            return { 'error': 'Review not found' }, 404
        
        response = {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id
        }
        return response, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        current_user = get_jwt_identity()
        """Update a review's information"""
        review_data = api.payload

        if current_user['id'] != review_data.get('user_id'):
            return {'error': 'Unauthorized action'}, 403
        
        # Checks if Review exists
        existing_review = facade.get_review(review_id)
        if not existing_review:
            return {'error': 'Review not found'}, 404
        try:
            facade.update_review(existing_review.id, review_data)
            return { 'message': 'Review successfully updated'}, 200
        except TypeError as e:
            return { 'error': str(e) }, 400
        except ValueError as e:
            return { 'error': str(e) }, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        current_user = get_jwt_identity()
        """Delete a review"""
        review = facade.get_review(review_id)
        if current_user['id'] != review.user.id:
            return {'error': 'Unauthorized action'}, 403
        
        if not review:
            return {'error': 'Review not found'}, 404
        facade.delete_review(review_id)
        return { 'message': 'Review details deleted successfully'}, 200
