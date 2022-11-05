import requests

pokemon_list = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1154')
poke_list = []
for n in pokemon_list.json()['results']:
    name = n['name']
    poke = requests.get(f'https://pokeapi.co/api/v2/pokemon-species/{name}')
    gen = poke.json()['generation']['name']
    poke_img = requests.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    img = poke_img.json()['sprites']['other']['official-artwork']['front_default']
    
    if gen.endswith('i'):
        gen = 1
    elif gen.endswith('ii'):
        gen = 2
    elif gen.endswith('iii'):
        gen = 3
    elif gen.endswith('iv'):
        gen = 4
    elif gen.endswith('v'):
        gen = 5
    elif gen.endswith('vi'):
        gen = 6
    elif gen.endswith('vii'):
        gen = 7
    elif gen.endswith('viii'):
        gen = 8
    poke_list.append([name, gen, img])
    # print(name)
    print(gen)
    # print(img)
    
# print(poke_list[0][2]) print specific items in list
    

print(poke_list)