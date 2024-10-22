from app.models.user import User
from app.models.place import Place

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=user)
    place2 = Place(title="True Apartment", description="A great place to stay", price=120, latitude=39.7749, longitude=-115.4194, owner=user)
    user.add_place(place)
    user.add_place(place2)
    print(f"El usuario es dueño de {user.places[0].title} y {user.places[1].title}")
    var = user.update(user.id, "axel", "palombo", "axel.palombo.ap@gmail.com")
    print(f"La funcion ha resultado en: {var}, los nuevos datos del usuario son {user.first_name} {user.last_name} y su correo es {user.email}")
    deleted_user = user.delete(user.id)
    print(deleted_user)
    new_user = User(first_name='Axel', last_name='$$$', email='axel.palombo.ap@gmail.com')
    print(f"{new_user.first_name} {new_user.last_name}")
test_user_creation()