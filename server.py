from flask import Flask, render_template, request, redirect, session
import requests
from database import sql_execute
import bcrypt
import os

secretkey = os.environ.get('sessionsecretkey')
app = Flask(__name__)
app.secret_key = secretkey


@app.route('/')
def main():
    if session.get('Gen') == None:
        session['Gen'] = 'All'
        select = 'All'
    else:
        select = session['Gen']
    
    if session.get("Logged_in") != True:
        session['Logged_in'] = False

    if session.get('login_name') is not None:
        login_name = session['login_name']
        admin = session['Admin']
    else:
        admin = False
        login_name = None
    if select == 'All':
        db_data = sql_execute('SELECT name, generation, image, pokedex FROM pokemon ORDER BY pokedex ASC')
    else:
        db_data = sql_execute('SELECT name, generation, image, pokedex FROM pokemon WHERE generation = %s ORDER BY pokedex ASC', [select])
    pokemon = []
    for dbdata in db_data:
        name, generation, image, pokedex = dbdata
        pokemon.append([name, generation, image, pokedex])
    return render_template('index.html', pokemon=pokemon, login_name=login_name, admin=admin, select=select)
  

@app.route('/', methods=["POST"])
def main_gen():
    select = request.form.get('gen_choice')
    
    name_search = request.form.get('pokesearch')
    if session.get('login_name') is not None:
        login_name = session['login_name']
        admin = session['Admin']
    else:
        admin = False
        login_name = None
    
    pokemon = []
    if name_search == "":
        if select == 'All':
            db_data = sql_execute('SELECT name, generation, image, pokedex FROM pokemon ORDER BY pokedex ASC')
            session['Gen'] = 'All'
            pokemon = []
            for dbdata in db_data:
                name, generation, image, pokedex = dbdata
                pokemon.append([name, generation, image, pokedex])
            return render_template('index.html', select=select, pokemon=pokemon, login_name=login_name)

        else:
            session['Gen'] = select
            db_data = sql_execute('SELECT name, generation, image, pokedex FROM pokemon WHERE generation = %s ORDER BY pokedex ASC', [select])
            for dbdata in db_data:
                name, generation, image, pokedex = dbdata
                pokemon.append([name, generation, image, pokedex])
            return render_template('index.html', select=select, pokemon=pokemon, login_name=login_name)
    else:
        db_data = sql_execute("SELECT name, generation, image, pokedex FROM pokemon WHERE name LIKE '%%' || %s || '%%' ORDER BY pokedex ASC", [name_search])
        print(db_data)
        for dbdata in db_data:
            name, generation, image, pokedex = dbdata
            pokemon.append([name, generation, image, pokedex])
        return render_template('index.html', select=select, pokemon=pokemon, login_name=login_name)


@app.route('/login', methods=["POST"])
def login():
    login_id = request.form.get('login_id')
    password = request.form.get('password')
    
    user_data = sql_execute('SELECT user_id, email, name, is_admin FROM users WHERE email = %s', [login_id])
    password_hash = sql_execute('SELECT pass_hash FROM users where email = %s', [login_id])
    
    if password_hash:
        valid = bcrypt.checkpw(password.encode(), password_hash[0][0].encode())
    else:
        error = "User or Pasword Incorrect"
        return render_template('login.html', error=error)
    
    
    for username in user_data:
        
        if login_id == username[1] and valid == True:
            response = redirect('/')
            loginName = session['login_name'] = username[2]
            user_id = session['Login_id'] = username[0]
            is_admin = session['Admin'] = username[3]
            is_loggedIn = session['Logged_in'] = True
    

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
        
        sql_execute('INSERT INTO users (name, pass_hash, is_admin, email) VALUES (%s, %s, False, %s)', [name, password_encrypt, email])
        return redirect('/')
    else:
        error = "Passwords did not match"
        return render_template('register.html', error=error)


@app.route('/<pokedexnum>')
def detailed(pokedexnum):
    int(pokedexnum)
    if session['Logged_in'] == True:
        login_name = session['login_name']
        user_id = session['Login_id']
        check_if_exist = sql_execute('SELECT * from favourites WHERE pokedex = %s and user_id = %s', [pokedexnum, user_id])
        pokemon_info = sql_execute('SELECT name, generation, image, pokedex FROM pokemon WHERE pokedex = %s', [pokedexnum])
    else:
        login_name = None
        check_if_exist = []
        pokemon_info = sql_execute('SELECT name, generation, image, pokedex FROM pokemon WHERE pokedex = %s', [pokedexnum])
    
    
    logged_in = session['Logged_in']
    poke_detail = []
    for poke in pokemon_info:
        name, generation, image, pokedex = poke
        poke_detail.append([name, generation, image, pokedex])
        
    
    return render_template('detailed.html', poke_detail=poke_detail, logged_in=logged_in, check_if_exist=check_if_exist, login_name=login_name)

@app.route('/<pokedexnum>', methods=["POST"])
def favourited(pokedexnum):
    pokemon_info = sql_execute('SELECT name, generation, image, pokedex FROM pokemon WHERE pokedex = %s', [pokedexnum])
    poke_detail = []
    for poke in pokemon_info:
        name, generation, image, pokedex = poke
        poke_detail.append([name, generation, image, pokedex])
    
    user = session['Login_id']
    
    sql_execute('INSERT INTO favourites (user_id, poke_name, poke_img, pokedex, poke_gen) VALUES (%s, %s, %s, %s, %s)', [user, name, image, pokedex, generation])
    return redirect(f'/{pokedexnum}')

@app.route('/removefav', methods=["POST"])
def remove_favourite():
    pokedexnum = request.form.get('pokedex')
    user_id = session['Login_id']
    sql_execute('DELETE FROM favourites WHERE pokedex = %s and user_id = %s', [pokedexnum, user_id])
    return redirect('/')

@app.route('/favourites')
def favourites_list():
    login_name = session['login_name']
    user_id = session['Login_id']
    db_data = sql_execute('SELECT poke_name, poke_gen, poke_img, pokedex FROM favourites WHERE user_id = %s ORDER BY pokedex ASC', [user_id])
    pokemon = []
    for dbdata in db_data:
        name, generation, image, pokedex = dbdata
        pokemon.append([name, generation, image, pokedex])
    return render_template('favourites.html', pokemon=pokemon, login_name=login_name)

if __name__ == '__main__':
    # from dotenv import load_dot_env
    app.run(debug=True)
