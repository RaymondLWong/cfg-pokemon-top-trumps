import base64
import random
import requests
import pokebase as pb


class Stats:
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


def get_sprite(url) -> str:
    return base64.b64encode(requests.get(url).content)


class Pokemon:
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
        print(stat)
        flat[stat['stat']['name']] = stat['base_stat']
    return flat


def get_stats(stats) -> Stats:
    flat = flatten_stats(stats)
    return Stats(
        hp=flat['hp'],
        attack=flat['attack'],
        defence=flat['defence'],
        special_attack=flat['special-attack'],
        special_defence=flat['special-defence'],
        speed=flat['speed'],
        accuracy=flat['accuracy'],
        evasion=flat['evasion'],
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


test = random.randrange(1, 151)
bulbasaur = create_pokemon(1)
print(bulbasaur)

