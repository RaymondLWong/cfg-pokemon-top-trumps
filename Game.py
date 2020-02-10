import pprint as pp
from Card import prompt_user_for_generation, get_random_pokemon
from colorama import Fore, Style

generation = prompt_user_for_generation()
pokemon = get_random_pokemon(generation)
coloured_name = f'{Fore.CYAN}{pokemon.name.capitalize()}{Style.RESET_ALL}'
print(f'You drew {coloured_name}!')
pp.pprint(pokemon)
