import pokebase as pb
from random import randrange
from typing import Mapping, List

from Card import Pokemon, create_pokemon


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


def get_static_generations_and_starters() -> dict:
    # types are always (grass, fire, water)
    starters = {
        1: {
            'names': ['Red', 'Green', 'Blue'],
            'starters': ['Bulbasaur', 'Charmander', 'Squirtle']
        },
        2: {
            'names': ['Gold', 'Silver', 'Crystal'],
            'starters': ['Chikorita', 'Cyndaquil', 'Totodile']
        },
        3: {
            'names': ['Ruby', 'Sapphire', 'Emerald'],
            'starters': ['Treecko', 'Torchic', 'Mudkip']
        },
        4: {
            'names': ['Diamond', 'Pearl', 'Platinum'],
            'starters': ['Turtwig', 'Chimchar', 'Piplup']
        },
        5: {
            'names': ['Black', 'White'],
            'starters': ['Snivy', 'Tepig', 'Oshawott']
        },
        6: {
            'names': ['X', 'Y'],
            'starters': ['Chespin', 'Fennekin', 'Froakie']
        },
        7: {
            'names': ['Sun', 'Moon'],
            'starters': ['Rowlet', 'Litten', 'Popplio']
        },
        8: {
            'names': ['Sword', 'Shield'],
            'starters': ['Grookey', 'Scorbunny', 'Sobble']
        }
    }
    return starters
