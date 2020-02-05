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


pokedex_number = random.randrange(1, 151)
random_pokemon = create_pokemon(1)
pprint(random_pokemon)

