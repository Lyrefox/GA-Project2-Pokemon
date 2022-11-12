# GA-Project2-Pokemon
![img](static/images/image_processing20210626-7167-doy57small.png)
## ![img](static/images/icons8-pokeball-color-32.png) GA Project Number 2 ![img](static/images/icons8-pokeball-color-32.png)


Here is a website where you can create a list of your favourite pokemon!
Users must be logged in to create a favoruite list.

Pokemon information was aquired used https://pokeapi.co/.
Its a great API that has every little bit of information on every pokemon so check it out!


### Project Plans
![img](static/images/icons8-pokemon.gif)



Create 2 tables, 1 for users and 1 for items that have been favourited.
favourites table will be pokemon name, pokemon image, user who favourited (which will be linked to id in user table)



1. Main page that shows a list of all the pokemon with images preferrably - Done
    - going through the api caused too many reuests to be made in a short period of time and cause flask to crash, it was also very slow gettign information that way. So i made a seperate python file that pushed all the data from the api i needed and put everything into a table in my database.
2. Click on pokemon to get more detailed information about that pokemon - Done
    - created seperate page that shows more information on the pokemon that wa selected (not much info, only what i originally took from the api but more information could be gotten by making some requests to the api. This page is where i added the favourite button as I didn't want 1 thousand favourite buttons on the main page.)
3. Create ability for users to login - Done
    created login and register page and added a button on login page to login as a guest.
4. create favourite button on detailed page for logged in users to be able to favourite pokemon - Done
5. create sort function that can filter pokemon on main page by predefined filters. - Done
6. Create search function - WIP
7. Create Database - Done
    - create database and tables to hold user info, pokemon info and people favourite pokemon.
    - run python script to fill in pokemon information from API.