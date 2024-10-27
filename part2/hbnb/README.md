# Holberton School - AirBnB

Holberton school project for second trimester students.
Creating an API similar to the AirBnB webpage, managing Users and Places with Amenities and Reviews

# Team Members
Axel Palombo - axel.palombo.ap@gmail.com
Marcos Pessano - 
Rodrigo Novelli - 

# API Documentation
https://app.swaggerhub.com/apis/AXELPALOMBOAP/HBNB/1.0.2

# API Structure explanation

This project structure works with four important folders that remain inside /App.

/App/:
    This folder contains all files of the project, configurations, requirements, tests and the Run module.

    /api/:
        Here we work the endpoints of our API, we got four namespaces or paths in our API; users, reviews, places and amenities with their respective requests.

    /models/:
        At this folder we have the models of our entities, every attribute and method of each class its in this folder.

    /persistence/:
        This is the layer that interacts with the DataBase, all operations like retrieving, updating or deletings data are in this folder.

    /services/:
        In services resides our facade, principal responsible of interacting with the rest of the code, it contains all the methods that this API uses to work

# Requirements

All the modules requireds for this API to work are contained in requirements.txt
To install required modules just write `pip install -r requirements.txt` in your terminal
Make sure you're standing on the /hbnb/ folder

# Running the server

To run the server, first make sure you have all the requirements installed.
Then just write `python3 run.py` in your terminal and the server will be working


