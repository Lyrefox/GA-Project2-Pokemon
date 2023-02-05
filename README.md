# GA-Project2-Pokemon
![img](static/images/image_processing20210626-7167-doy57small.png)
## ![img](static/images/icons8-pokeball-color-32.png) GA Project Number 2 ![img](static/images/icons8-pokeball-color-32.png)


https://pokemon-favourites.herokuapp.com/  -- Currently Down, General Assembly working on a Solution

Here is a website where you can create a list of your favourite pokemon!
Users must be logged in to create a favoruite list.

Pokemon information was aquired used https://pokeapi.co/.
Its a great API that has every little bit of information on every pokemon so check it out!


### Project Plans
![img](static/images/icons8-pokemon.gif)

1. Main page that shows a list of all the pokemon with images preferrably - Done
    - going through the api caused too many reuests to be made in a short period of time and cause flask to crash, it was also very slow gettign information that way. So i made a seperate python file that pushed all the data from the api i needed and put everything into a table in my database.
2. Click on pokemon to get more detailed information about that pokemon - Done
    - created seperate page that shows more information on the pokemon that wa selected (not much info, only what i originally took from the api but more information could be gotten by making some requests to the api. This page is where i added the favourite button as I didn't want 1 thousand favourite buttons on the main page.)
3. Create ability for users to login - Done
    created login and register page and added a button on login page to login as a guest.
4. create favourite button on detailed page for logged in users to be able to favourite pokemon - Done
    - created favourite button that added pokemon to the favourites table in the table based on the id of the user currently logged in. Button changes to un-favourite once favourited and clicking will delete the pokemon from the favorourites table based on the user id. Link on main page will show up if user is logged in that will show all the pokemon you have favourited.
5. create sort function that can filter pokemon on main page by predefined filters. - Done
    - created filter that allows users to filter the wide selection of pokemon based on the generation they are from.
6. Create search function - Done
    - I have tried adding a search function so you can search for specific pokemon but couldn't get the interaction between python and SQL formatting correct. So search bar is hidden for time being.
7. Create Database - Done
    - create database and tables to hold user info, pokemon info and people favourite pokemon.
    - run python script to fill in pokemon information from API.
