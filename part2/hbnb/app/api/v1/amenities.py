from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

facade = HBnBFacade()

# Post Creates an Amenity / Get gets all Amenities
@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = api.payload

        try:
            new_amenity = facade.create_amenity(data)
            return {'id': new_amenity.id, 'name': new_amenity.name }, 201
        except TypeError as e:
            return {'error': str(e)}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities_list = facade.get_all_amenities()
        if not amenities_list:
            return { 'error': 'No amenities found' }, 404
        return amenities_list, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return { 'error': 'Amenity not found' }, 404
        return { 'id': amenity.id, 'name': amenity.name }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Amenity not found')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload

        # Checks if User exists
        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            return {'error': 'Amenity not found'}, 400
        try:
            amenity_name = amenity_data.get('name')
            facade.update_amenity(existing_amenity.id, amenity_name)
            return { 'message': 'Amenity updated successfully'}, 200
        except TypeError as e:
            return { 'error': str(e) }, 400
        except ValueError as e:
            return { 'error': str(e) }, 400
        
    @api.response(200, 'Amenity details deleted successfully')
    @api.response(400, 'Invalid input data')
    def delete(self, amenity_id):
        """Get user details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        facade.delete_amenity(amenity_id)
        return { 'message': 'Amenity details deleted successfully'}, 200