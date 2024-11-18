from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized action')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        """Register a new place"""
        data = api.payload

        if current_user['id'] != data.get('owner_id'):
            return {'error': 'Unauthorized action'}, 403

        try:
            new_place = facade.create_place(data)
            return {
                "id": new_place.id,
                "title": new_place.title,
                "description": new_place.description or "No description found",
                "price": new_place.price,
                "latitude": new_place.latitude,
                "longitude": new_place.longitude,
                "owner_id": new_place.owner.id
                }, 201
        except TypeError as e:
            return {'error': str(e)}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    @api.response(404, 'No places found')
    def get(self):
        """Retrieve a list of all places"""
        places_list = facade.get_all_places()
        if not places_list:
            return { 'error': 'No places found' }, 404
        return places_list, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)

        if not place:
            return { 'error': 'Place not found'}, 404
        
        response = {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": {
            "id": place.owner.id,
            "first_name": place.owner.first_name,
            "last_name": place.owner.last_name,
            "email": place.owner.email
            },
        "amenities": [
            {"id": amenity.id, "name": amenity.name} for amenity in place.amenities
            ]
        }
        return response, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        """Register a new place"""
        data = api.payload

        if not is_admin and current_user['id'] != data.get('owner_id'):
            return {'error': 'Unauthorized action'}, 403

        # Checks if Place exists
        existing_place = facade.get_place(place_id)
        if not existing_place:
            return {'error': 'Place not found'}, 404
        try:
            facade.update_place(existing_place.id, data)
            return { 'message': 'Place successfully updated'}, 200
        except TypeError as e:
            return { 'error': str(e) }, 400
        except ValueError as e:
            return { 'error': str(e) }, 400
        
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        """Delete a place"""
        place = facade.get_place(place_id)
        if not is_admin and current_user['id'] != place.owner.id:
            return {'error': 'Unauthorized action'}, 403
        
        if not place:
            return {'error': 'Place not found'}, 404
        facade.delete_place(place_id)
        return { 'message': 'Place details deleted successfully'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)

        if not place:
            return { 'error': 'Place not found' }, 404
        
        review_list = facade.get_reviews_by_place(place_id)
        if len(review_list) == 0:
            return { 'message': 'No reviews in this place' }, 200
        return review_list, 200