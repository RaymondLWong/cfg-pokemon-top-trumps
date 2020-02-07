import pprint as pp
from Card import prompt_user_for_generation, get_random_pokemon

generation = prompt_user_for_generation()
pokemon = get_random_pokemon(generation)
print(f'You drew {pokemon.name.capitalize()}!')
pp.pprint(pokemon)
