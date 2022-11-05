import requests
import psycopg2
conn = psycopg2.connect("dbname=pokemon_favourites")
cur = conn.cursor()
pokemon_list = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1154')
# poke_list = []
for n in pokemon_list.json()['results']:
    
    name = n['name']
    poke = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name}')
    
    try:
        gen = poke.json()['generation']['name']
        id = poke.json()['id']

        img = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png'
        
        generation = {
            'generation-i': 1,
            'generation-ii': 2,
            'generation-iii': 3,
            'generation-iv': 4,
            'generation-v': 5,
            'generation-vi': 6,
            'generation-vii': 7,
            'generation-viii': 8,
        }
        gen = generation.get(gen)
        # print(gen)
        cur.execute('INSERT INTO pokemon (name, generation, image, pokedex) VALUES (%s, %s, %s, %s)', [name, gen, img, id])
        conn.commit()
        # poke_img = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
        # img = poke_img.json()['sprites']['other']['official-artwork']['front_default']
        
        # gen = 1
        # elif gen == 'generation-ii':
        #     gen = 2
        # elif gen == 'generation-iii':
        #     gen = 3
        # elif gen == 'generation-iv':
        #     gen = 4
        # elif gen == 'generation-v':
        #     gen = 5
        # elif gen == 'generation-vi':
        #     gen = 6
        # elif gen == 'generation-vii':
        #     gen = 7
        # elif gen == 'generation-viii':
        #     gen = 8
        
        # poke_list.append([name, gen, img, pokedex_number])
        
        print(name)
        print(gen)
        print(img)
        
    except:
        print(poke.status_code, poke.text)
cur.close()
conn.close()
# print(poke_list[0][2]) print specific items in list
    

# print(poke_list)