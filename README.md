## Capstone project

I used the render platform to deploy my flask app

The base url for api: https://fsnd-final-project.onrender.com

We will use postman to call each API below

- To get all movies: https://fsnd-final-project.onrender.com/movies (GET)
- To get all actors: https://fsnd-final-project.onrender.com/actors (GET)
- To create a new movie: https://fsnd-final-project.onrender.com/movies (POST)
- To create a new actor: https://fsnd-final-project.onrender.com/actors (POST)
- To update a movie: https://fsnd-final-project.onrender.com/movies/<movie_id> (PATCH)
- To update an actor: https://fsnd-final-project.onrender.com/actors/<actor_id> (PATCH)
- To delete a movie: https://fsnd-final-project.onrender.com/movies/<movie_id> (DELETE)
- To delete an actor: https://fsnd-final-project.onrender.com/actors/<actor_id> (DELETE)

I have created three users with different roles:
- Casting Assistant: Can view actors and movies
- Casting Director:	All permissions a Casting Assistant has and Add or delete an actor from the database Modify actors or movies
- Executive Producer: All permissions a Casting Director has and Add or delete a movie from the database

To get the jwt token for each user:
 - Please go to the following url: https://dev-wpvjr6p5aq21gtxe.us.auth0.com/authorize?audience=http://127.0.0.1:5001/&response_type=token&client_id=cLJLlK2VtwFVSOYSTjI1st6s79rNJj3r&redirect_uri=https://fsnd-final-project.onrender.com/

 - For Casting Assistant, please use the following email and password:
   - Email: castingassistant@email.com
   - Password: user1@a.
 
 - For Casting Director, please use the following email and password:
    - Email: castingdirector@email.com
    - Password: user1@a.
 
 - For Executive Producer, please use the following email and password:
    - Email: executiveproducer@email.com
    - Password: user1@a.
 
After logining successfully, you will see the url like that: https://fsnd-final-project.onrender.com/#access_token=exampletokens&expires_in=7200&token_type=Bearer
Please copy the value of access_token and use postman to call the API.