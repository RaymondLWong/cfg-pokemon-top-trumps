import itertools
import math
from copy import copy

import requests
import pprint as pp
import pokebase as pb
from src.gameplay.image_to_ascii_art import image_to_ascii_art
from colorama import Fore, Style
from typing import Generic, TypeVar, List, Union

T = TypeVar('T')


def get_available_props(dictionary: dict) -> dict:
    dict_copy = {}
    for key, value in dictionary.items():
        if isinstance(value, Entry):
            if value.value is not None:
                dict_copy.update({key: value})
        elif value is not None:
            dict_copy.update({key: value})
    return dict_copy


def format_as_table(dictionary: dict, columns: int = 2, label_offset: int = 0) -> str:
    rows = math.ceil(len(dictionary) / columns)
    labels = [label_offset + x * rows for x in range(columns)]
    table = ''
    for index, (key, entry) in enumerate(dictionary.items()):
        col = index % columns
        entry_is_class = isinstance(entry, Entry)
        if entry_is_class and isinstance(entry.value, int):
            labels[col] += 1
            dictionary[key].shortcut = labels[col]
        value = entry.value if entry_is_class else entry
        end = '\n' if index % columns == 1 else ''
        table += '{:<17} {:<7}{}'.format(key, value, end)
    return f'\n{table}'


class PrettyClass:
    def __repr__(self):
        return pp.pformat(vars(self))


class Sprite:
    def __init__(self, ascii_art, show_avatar: bool = True):
        self.ascii_art = ascii_art
        self.show_avatar = show_avatar

    def __repr__(self):
        return self.ascii_art if self.show_avatar else None


class Entry:
    def __init__(
            self,
            name: str,
            value: int,
            shortcut: int = -1
    ):
        self.name = name
        self.value = value
        self.shortcut = shortcut

    def __repr__(self):
        return pp.pformat(self.value)


class Stats(PrettyClass, Generic[T]):
    def __init__(
            self,
            hp: T,
            attack: T,
            defence: T,
            special_attack: T,
            special_defence: T,
            speed: T,
            accuracy: T,
            evasion: T
    ):
        self.hp = Entry('hp', hp)
        self.attack = Entry('attack', attack)
        self.defence = Entry('defence', defence)
        self.special_attack = Entry('special_attack', special_attack)
        self.special_defence = Entry('special_defence', special_defence)
        self.speed = Entry('speed', speed)
        self.accuracy = Entry('accuracy', accuracy)
        self.evasion = Entry('evasion', evasion)

    def __repr__(self):
        props_as_dict = vars(self)
        avail_stats = get_available_props(props_as_dict)
        return format_as_table(avail_stats, label_offset=3)


def get_sprite(url) -> Sprite:
    image_data = requests.get(url).content
    ascii_art = image_to_ascii_art(image_data)
    return Sprite(ascii_art)


class Pokemon(PrettyClass):
    def __init__(self, poke_id: int, name: str, height: int, weight: int, sprite: str, stats: Stats[Entry]):
        self.poke_id = Entry('poke_id', poke_id)
        self.name = name.capitalize()
        self.height = Entry('height', height)
        self.weight = Entry('weight', weight)
        self.sprite = get_sprite(sprite)
        self.stats = stats
        self.str_repr = self.determine_str_repr()

    def determine_str_repr(self) -> str:
        sorted_props = {}
        sorted_props.update({'poke_id': self.poke_id})
        sorted_props.update({'name': f'{Fore.CYAN}{self.name}{Style.RESET_ALL}'})
        sorted_props.update({'height': self.height})
        sorted_props.update({'weight': self.weight})
        all_props = f'\n{self.sprite}\n' if self.sprite else ''
        return all_props + format_as_table(sorted_props) + self.stats.__str__()

    def __repr__(self):
        return self.str_repr

    def __iter__(self):
        base_info = {
            'poke_id': self.poke_id,
            'name': self.name,
            'height': self.height,
            'weight': self.weight
        }
        return itertools.chain(base_info, self.stats)

    def __getitem__(self, item):
        p = vars(copy(self))
        for stat_name, stat in vars(p['stats']).items():
            p[stat_name] = stat
        return p[item]

    def get_available_battle_stats(self, as_string: bool) -> List[Union[str, Entry]]:
        battle_stats = []
        all_stats = dict(vars(self))  # make a copy, instead of mutating
        for entry in all_stats.values():
            if isinstance(entry, Entry):
                battle_stats.append(entry)
            elif isinstance(entry, Stats):
                for stat in vars(entry).values():
                    battle_stats.append(stat)

        available_stats = []
        # filter empty stats
        for entry in battle_stats:
            if entry.value:
                available_stats.append(entry.name if as_string else entry)
        return available_stats


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
        hp=flat.get('hp', None),
        attack=flat.get('attack', None),
        defence=flat.get('defense', None),
        special_attack=flat.get('special-attack', None),
        special_defence=flat.get('special-defense', None),
        speed=flat.get('speed', None),
        accuracy=flat.get('accuracy', None),
        evasion=flat.get('evasion', None)
    )


def create_pokemon(poke_id: int) -> Pokemon:
    info = pb.pokemon(poke_id)
    sprite = info.sprites.front_default
    stats = get_stats(info.stats)
    return Pokemon(
        poke_id,
        info.name,
        info.height,
        info.weight,
        sprite,
        stats
    )
