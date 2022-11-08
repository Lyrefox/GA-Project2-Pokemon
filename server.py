from flask import Flask, render_template, request, redirect, session
import requests
from database import sql_execute
import bcrypt
import os
import psycopg2
secretkey = os.environ.get('sessionsecretkey')
app = Flask(__name__)
app.secret_key = secretkey

@app.route('/')
def main():
    if session.get("Logged_in") != True:
        session['Logged_in'] = False

    if session.get('login_name') is not None:
        login_name = session['login_name']
        admin = session['Admin']
    else:
        admin = False
        login_name = None
    db_data = sql_execute('SELECT name, generation, image, pokedex FROM pokemon ORDER BY pokedex ASC')
    pokemon = []
    for dbdata in db_data:
        name, generation, image, pokedex = dbdata
        pokemon.append([name, generation, image, pokedex])
    return render_template('index.html', pokemon=pokemon, login_name=login_name, admin=admin)
  

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


@app.route('/login', methods=["POST"])
def login():
    login_id = request.form.get('login_id')
    password = request.form.get('password')

    user_data = sql_execute('SELECT user_id, email, name, is_admin FROM users WHERE email = %s', [login_id])
    password_hash = sql_execute('SELECT pass_hash FROM users where email = %s', [login_id])[0][0]
    valid = bcrypt.checkpw(password.encode(), password_hash.encode())
    
    
    for username in user_data:
        print(username[2])
        if login_id == username[1] and valid == True:
            response = redirect('/')
            loginName = session['login_name'] = username[2]
            user_id = session['Login_id'] = username[0]
            is_admin = session['Admin'] = username[3]
            is_loggedIn = session['Logged_in'] = True
            print(is_admin)
            print(user_id)
            print(loginName)

            return response
        else:
                error = "User or Pasword Incorrect"
                return render_template('login.html', error=error)

@app.route('/login')
def login_form():
    return render_template('login.html')

@app.route('/logout')
def logout():
    response = redirect('/')
    session.pop('login_name', None)
    session.pop('Login_id', None)
    session.pop('Admin', None)
    session.pop('Logged_in', None)
    return response

@app.route('/guest', methods=["POST"])
def guest_login():

    session['login_name'] = 'Guest'
    session['Login_id'] = 2
    session['Admin'] = False
    session['Logged_in'] = True
    return redirect('/')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register', methods=["POST"])
def register_acc():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    retypepassword = request.form.get('retypepassword')
    if password == retypepassword:
        password_encrypt = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(password_encrypt)
        sql_execute('INSERT INTO users (name, pass_hash, is_admin, email) VALUES (%s, %s, False, %s)', [name, password_encrypt, email])
        return redirect('/')
    else:
        error = "Passwords did not match"
        return render_template('register.html', error=error)


@app.route('/<pokedexnum>')
def detailed(pokedexnum):
    int(pokedexnum)
    login_name = session['login_name']
    pokemon_info = sql_execute('SELECT name, generation, image, pokedex FROM pokemon WHERE pokedex = %s', [pokedexnum])
    check_if_exist = sql_execute('SELECT * from favourites WHERE pokedex = %s', [pokedexnum])
    print(check_if_exist)
    poke_detail = []
    for poke in pokemon_info:
        name, generation, image, pokedex = poke
        poke_detail.append([name, generation, image, pokedex])
        logged_in = session['Logged_in']
        # print(logged_in)
    return render_template('detailed.html', poke_detail=poke_detail, logged_in=logged_in, check_if_exist=check_if_exist, login_name=login_name)

@app.route('/<pokedexnum>', methods=["POST"])
def favourited(pokedexnum):
    pokemon_info = sql_execute('SELECT name, generation, image, pokedex FROM pokemon WHERE pokedex = %s', [pokedexnum])
    poke_detail = []
    for poke in pokemon_info:
        name, generation, image, pokedex = poke
        poke_detail.append([name, generation, image, pokedex])
    print(name, generation, image, pokedex)
    user = session['Login_id']
    print(user)
    # sql_execute('INSERT INTO favourites (user_id, poke_name, poke_img, pokedex, poke_gen) VALUES (%s, %s, %s, %s, %s)', [user, name, image, pokedex, generation])
    return redirect(f'/{pokedexnum}')

@app.route('/removefav', methods=["POST"])
def remove_favourite():
    pokedexnum = request.form.get('pokedex')
    print(pokedexnum)
    return "Test"

if __name__ == '__main__':
    # from dotenv import load_dot_env
    app.run(debug=True)
