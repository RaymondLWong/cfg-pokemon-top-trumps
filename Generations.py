import requests
from random import random
from typing import Mapping
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
    gen_relative_poke_id = random.randrange(1, get_static_pokemon_count_for_generation(gen))
    poke_id = get_poke_id(gen, gen_relative_poke_id)
    pokemon_card = create_pokemon(poke_id)
    return pokemon_card
