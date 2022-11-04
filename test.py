import requests
import pokebase as pb
pokemon_list = requests.get('https://pokeapi.co/api/v2/pokemon?limit=1154')
# gen_choice = 3
gen_choice = input('Enter a generation number: ')
pokemon_gen = requests.get(f'https://pokeapi.co/api/v2/generation/{gen_choice}')
# i = 1
# while i < len(test.json()['results']):
#     pokename = test.json()['results'][i]['name']
#     print(pokename)
#     i += 1

# for i in pokemon_list.json()['results']:
#     poke = i['name']
#     poke_info = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke}')
#     poke_img = poke_info.json()['sprites']['front_default']
    


for n in pokemon_gen.json()['pokemon_species']:
    poke = n['name']
    print(poke)


# s1 = pb.SpriteResource('pokemon', 23)
# print(s1.url)

# ditto = pb.pokemon('charmander')
# print(ditto.height)