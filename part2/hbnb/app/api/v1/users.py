from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

facade = HBnBFacade()

# POST Sign up -> Checks Email registration / GET all User list
@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        try:
            new_user = facade.create_user(user_data)
            return {'id': new_user.id, 'first_name': new_user.first_name, 'last_name': new_user.last_name, 'email': new_user.email}, 201
        except TypeError as e:
            return {'error': str(e)}, 400
        except ValueError as e:
            return {'error': str(e)}, 400
        
    @api.response(200, 'Users successfully retrieved')
    @api.response(404, 'No users found')
    def get(self):
        """Get all users"""
        users_list = facade.get_users_list()
        if not users_list:
            return { 'error': 'No users found'}, 404
        return users_list, 200
        
# GET User by ID
@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.response(201, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Updates an User"""
        user_data = api.payload

        # Checks if User exists
        existing_user = facade.get_user(user_id)
        if not existing_user:
            return {'error': 'User not found'}, 400
        try:
            facade.update_user(existing_user.id, user_data)
            return { 'message': 'User successfully updated'}, 200
        except TypeError as e:
            return { 'error': str(e) }, 400
        except ValueError as e:
            return { 'error': str(e) }, 400
    
    @api.response(200, 'User details deleted successfully')
    @api.response(400, 'Invalid input data')
    def delete(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        facade.delete_user(user_id)
        return { 'message': 'User details deleted successfully'}, 200

# PUT Update User places
@api.route('/add_place') # { 'email': string, 'place_id': string} Email y Nombre del lugar
class UserAddPlace(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'Place added to the user')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @api.response(404, 'Place not found')
    def put(self):
        """Adds a place to a user"""
        data = api.payload

        # Checks the req body
        if not data['email'] or not data['place_id']:
            return { 'error': 'Invalid input data' }, 400
        # Checks if User exists
        existing_user = facade.get_user_by_email(data['email'])
        if not existing_user:
            return { 'error': 'User not found' }, 404
        # Checks if Place exists
        place = facade.get_place(data['place_id'])
        if not place:
            return { 'error': 'Place not found' }, 404
        # We add the place to the User
        facade.add_user_place(existing_user.id, place.id)
        return { 'Place added to the user' }, 200
