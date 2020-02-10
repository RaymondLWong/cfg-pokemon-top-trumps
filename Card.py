import random
import pprint as pp
import requests
import pokebase as pb
import math
from image_to_ascii_art import image_to_ascii_art
from colorama import Fore, Style


def get_available_props(dictionary: dict) -> dict:
    copy = {}
    for key, value in dictionary.items():
        if value != -1:
            copy.update({key: value})
    return copy


def format_as_table(dictionary: dict, columns: int = 2, label_offset: int = 0) -> str:
    rows = math.ceil(len(dictionary) / columns)
    labels = [label_offset + x * rows for x in range(columns)]
    table = ''
    for index, (key, value) in enumerate(dictionary.items()):
        end = '\n' if index % columns == 1 else ''
        col = index % columns
        labels[col] += 1
        table += '{:<3} {:<17} {:<7}{}'.format(f'{labels[col]})', key, value, end)
    return f'\n{table}'


class PrettyClass:
    def __repr__(self):
        return pp.pformat(vars(self))


class Sprite:
    def __init__(self, ascii_art):
        self.ascii_art = ascii_art

    def __repr__(self):
        return self.ascii_art


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

    def __repr__(self):
        stats_as_dict = vars(self)
        avail_stats = get_available_props(stats_as_dict)
        return format_as_table(avail_stats, label_offset=4)


def get_sprite(url) -> Sprite:
    image_data = requests.get(url).content
    ascii_art = image_to_ascii_art(image_data)
    return Sprite(ascii_art)


class Pokemon(PrettyClass):
    def __init__(self, poke_id: int, name: str, height: int, weight: int, sprite: str, stats: Stats):
        self.poke_id = poke_id
        self.name = name
        self.height = height
        self.weight = weight
        self.sprite = get_sprite(sprite)
        self.stats = stats

    def __repr__(self):
        sorted_props = {}
        sorted_props.update({'poke_id': self.poke_id})
        sorted_props.update({'name': f'{Fore.CYAN}{self.name.capitalize()}{Style.RESET_ALL}'})
        sorted_props.update({'height': self.height})
        sorted_props.update({'weight': self.weight})
        all_props = f'\n{self.sprite}\n'
        all_props += format_as_table(sorted_props)
        all_props += self.stats.__str__()
        return all_props


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
