from flask import Flask, render_template, request, redirect
import requests
from database import sql_execute

app = Flask(__name__)
@app.route('/')
def main():
    db_data = sql_execute('SELECT name, generation, image, pokedex FROM pokemon ORDER BY pokedex ASC')
    pokemon = []
    for dbdata in db_data:
        name, generation, image, pokedex = dbdata
        pokemon.append([name, generation, image, pokedex])
    return render_template('index.html', pokemon=pokemon)

@app.route('/', methods=["POST"])
def main_gen():
    select = request.form.get('gen_choice')
    print(select)
    name_search = request.form.get('pokesearch')
    print(name_search)
    # print(name)
    pokemon = []
    if name_search == "":
        if select == 'all':
            db_data = sql_execute('SELECT name, generation, image, pokedex FROM pokemon ORDER BY pokedex ASC')
            pokemon = []
            for dbdata in db_data:
                name, generation, image, pokedex = dbdata
                pokemon.append([name, generation, image, pokedex])
            return render_template('index.html', select=select, pokemon=pokemon)
        else:
            db_data = sql_execute('SELECT name, generation, image, pokedex FROM pokemon WHERE generation = %s ORDER BY pokedex ASC', [select])
            for dbdata in db_data:
                name, generation, image, pokedex = dbdata
                pokemon.append([name, generation, image, pokedex])
            return render_template('index.html', select=select, pokemon=pokemon)
    else:
        db_data = sql_execute(f'SELECT name, generation, image, pokedex FROM pokemon WHERE name = %s ORDER BY pokedex ASC', [name_search])
        print(db_data)
        for dbdata in db_data:
            name, generation, image, pokedex = dbdata
            pokemon.append([name, generation, image, pokedex])
        return render_template('index.html', select=select, pokemon=pokemon)

@app.route('/login')
def login_form():
    return render_template('login/html')

@app.route('/login', methods=["POST"])
def login():
    return


if __name__ == '__main__':
    # from dotenv import load_dot_env
    app.run(debug=True)
