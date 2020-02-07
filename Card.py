import random
from pprint import pprint

import requests
import pokebase as pb
from image_to_ascii_art import image_to_ascii_art


class PrettyClass:
    def __repr__(self):
        return repr(vars(self))


class Sprite:
    def __init__(self, ascii_art):
        self.ascii_art = ascii_art

    def __repr__(self):
        return '\n' + self.ascii_art + '\n'


class Stats(PrettyClass):
    def __init__(
            self,
            hp: int,
            attack: int,
            defence: int,
            special_attack: int,
            special_defence: int,
            speed: int,
            accuracy: int,
            evasion: int
    ):
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.special_attack = special_attack
        self.special_defence = special_defence
        self.speed = speed
        self.accuracy = accuracy
        self.evasion = evasion


def get_sprite(url) -> Sprite:
    image_data = requests.get(url).content
    ascii_art = image_to_ascii_art(image_data)
    return Sprite(ascii_art)


class Pokemon(PrettyClass):
    def __init__(self, pokedex_entry: int, name: str, height: int, weight: int, sprite: str, stats: Stats):
        self.pokedex_entry = pokedex_entry
        self.name = name
        self.height = height
        self.weight = weight
        self.sprite = get_sprite(sprite)
        self.stats = stats


def flatten_stats(stats):
    flat = {}
    for stat in stats:
        stat_name = stat.stat.name
        stat_value = stat.base_stat
        flat[stat_name] = stat_value
    return flat


def get_stats(stats) -> Stats:
    flat = flatten_stats(stats)
    return Stats(
        hp=flat.get('hp', -1),
        attack=flat.get('attack', -1),
        defence=flat.get('defense', -1),
        special_attack=flat.get('special-attack', -1),
        special_defence=flat.get('special-defense', -1),
        speed=flat.get('speed', -1),
        accuracy=flat.get('accuracy', -1),
        evasion=flat.get('evasion', -1)
    )


def create_pokemon(pokedex_entry) -> Pokemon:
    info = pb.pokemon(pokedex_entry)
    sprite = info.sprites.front_default
    stats = get_stats(info.stats)
    return Pokemon(
        pokedex_entry,
        info.name,
        info.height,
        info.weight,
        sprite,
        stats
    )


def get_available_generations() -> int:
    # warning, there's an API limit of 100 / minute, so avoid using this function too often
    results = requests.get('https://pokeapi.co/api/v2/generation/').text
    return int(results.count)


def get_static_pokemon_count_for_generation(gen: int) -> int:
    generations = {
        1: 151,
        2: 100,
        3: 135,
        4: 107,
        5: 156,
        6: 72,
        7: 81
    }
    return generations[gen] or -1


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


def prompt_user_for_generation() -> int:
    user_picked_gen = input('Pick a generation between 1-7: ')
    try:
        gen = int(user_picked_gen)
        print(f'You chose Generation {gen}!')
        return gen
    except ValueError:
        print('Defaulting to Generation 1...')
        return 1


generation = prompt_user_for_generation()
pokemon = get_random_pokemon(generation)
print(f'You drew {pokemon.name.capitalize()}!')
pprint(pokemon)

