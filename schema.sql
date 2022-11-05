DROP TABLE IF EXISTS pokemon_favourites;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT,
    pass_hash TEXT,
    is_admin BOOLEAN
);

CREATE TABLE favourites (
    fav_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    poke_name TEXT,
    poke_img TEXT,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);