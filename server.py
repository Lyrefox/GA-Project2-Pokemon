from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/', methods=["POST"])
def main_gen():
    select = request.form.get('gen_choice')
    print(select)
    pokemon_gen = requests.get(f'https://pokeapi.co/api/v2/generation/{select}')
    pokemon = []
    for n in pokemon_gen.json()['pokemon_species']:
        name = n['name']
        # poke_img = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
        # img = poke_img.json()['sprites']['other']['official-artwork']['front_default']
        # print(img)
        pokemon.append(name)
        
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
