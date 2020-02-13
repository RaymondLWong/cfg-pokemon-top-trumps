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
    starters = {
        1: {
            'icons': ['🟥', '🟩', '🟦'],
            'names': ['Red', 'Green', 'Blue'],
            'starters': ['Bulbasaur', 'Charmander', 'Squirtle']
        },
        2: {
            'icons': ['🏅', '🥈', '💎'],
            'names': ['Gold', 'Silver', 'Crystal'],
            'starters': ['Chikorita', 'Cyndaquil', 'Totodile']
        },
        3: {
            'icons': ['♦️', '🔷', '❇️️'],  # ✳️☘️
            'names': ['Ruby', 'Sapphire', 'Emerald'],
            'starters': ['Treecko', 'Torchic', 'Mudkip']
        },
        4: {
            'icons': ['🔶', '⚪', '⛓️'],
            'names': ['Diamond', 'Pearl', 'Platinum'],
            'starters': ['Turtwig', 'Chimchar', 'Piplup']
        },
        5: {
            'icons': ['🏴', '🏳️'],
            'names': ['Black', 'White'],
            'starters': ['Snivy', 'Tepig', 'Oshawott']
        },
        6: {
            'icons': ['✖️', '🆈'],  # 🇾 🆈 ץ ㄚ ¥ ⓨ
            'names': ['X', 'Y'],
            'starters': ['Chespin', 'Fennekin', 'Froakie']
        },
        7: {
            'icons': ['☀️', '🌙'],
            'names': ['Sun', 'Moon'],
            'starters': ['Rowlet', 'Litten', 'Popplio']
        },
        8: {
            'icons': ['⚔️', '️🛡️'],
            'names': ['Sword', 'Shield'],
            'starters': ['Grookey', 'Scorbunny', 'Sobble']
        }
    }
    return starters


def fancy_starter(text: str, wrapper: str) -> str:
    return '{} {:<10}'.format(wrapper, text, wrapper)


def get_starters_as_str(starters: [str, str, str]) -> str:
    # types are always (grass, fire, water)
    return ' '.join([
        fancy_starter(starters[0], '🌱'),
        fancy_starter(starters[1], '🔥'),
        fancy_starter(starters[2], '💧')
    ])


def get_available_generations() -> List[dict]:
    generations_and_starters = get_static_generations_and_starters()
    available_generations = []
    for gen_no, gen in generations_and_starters.items():
        game_names = ', '.join(gen['names'])
        # icons = ' '.join(gen['icons'])  # icons mess up alignment :(
        gen_name_and_starters = 'Gen {}: {:<25} (starters: {:<})'.format(
            gen_no,
            game_names,
            get_starters_as_str(gen['starters'])
        )
        available_generations.append({
            'name': gen_name_and_starters,
            'value': gen_no
        })
    return available_generations
