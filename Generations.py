import requests
import pokebase as pb
from random import randrange
from typing import Mapping, List

from Card import Pokemon, create_pokemon


def get_available_generations() -> int:
    # warning, there's an API limit of 100 / minute, so avoid using this function too often
    results = requests.get('https://pokeapi.co/api/v2/generation/').text
    return int(results.count)


def get_static_generation_counts() -> Mapping[int, int]:
    return {
        1: 151,
        2: 100,
        3: 135,
        4: 107,
        5: 156,
        6: 72,
        7: 81
    }


def get_static_pokemon_count_for_generation(gen: int) -> int:
    generations = get_static_generation_counts()
    return generations[gen]


def get_poke_id(gen: int, relative_id: int) -> int:
    past_gen_count = 0
    for cumulative_gen in range(1, gen):
        past_gen_count += get_static_pokemon_count_for_generation(cumulative_gen)
    return past_gen_count + relative_id


def get_random_pokemon(gen: int) -> Pokemon:
    gen_relative_poke_id = randrange(1, get_static_pokemon_count_for_generation(gen) + 1)
    poke_id = get_poke_id(gen, gen_relative_poke_id)
    pokemon_card = create_pokemon(poke_id)
    return pokemon_card


def get_types(pokemon_types: List[dict]) -> List[str]:
    avail_types = []
    for pokemon_type in pokemon_types:
        avail_types.append(pokemon_type.type.name)
    return avail_types


def colour_pokemon_name_by_its_types(name: str, types: List[str]) -> str:
    # TODO: use 'colorama library to colour the name
    return name


def get_starter_pokemon(gen: int) -> List[dict]:
    starters = []
    print(f'Fetching Gen {gen} starters from PokeAPI', end='')
    for i in range(1, 3*3, 3):
        pokemon = pb.pokemon(get_poke_id(gen, i))
        print('.', end='')
        starters.append(pokemon)
    print()

    return starters


def get_starter_pokemon_names(gen: int) -> List[str]:
    starter_pokemon = []
    for starter in get_starter_pokemon(gen):
        pokemon_types = get_types(starter.types)
        pokemon_name: str = colour_pokemon_name_by_its_types(starter.name, pokemon_types)
        starter_pokemon.append(pokemon_name.capitalize())
    return starter_pokemon


def get_static_starter_pokemon_names() -> dict:
    # types are always (grass, fire, water)
    starters = {
        1: ['Bulbasaur', 'Charmander', 'Squirtle'],
        2: ['Chikorita', 'Cyndaquil', 'Totodile'],
        3: ['Bulbasaur', 'Charmander', 'Squirtle'],  # same as Gen 1
        4: ['Chikorita', 'Cyndaquil', 'Totodile'],  # same as Gen 2
        5: ['Snivy', 'Tepig', 'Oshawott'],
        6: ['Chespin', 'Fennekin', 'Froakie'],
        7: ['Rowlet', 'Litten', 'Popplio'],
        8: ['Grookey', 'Scorbunny', 'Sobble']
    }
    return starters
