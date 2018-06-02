from tdl.map import Map
from random import randint
from entity import Entity
from components.ai import BasicMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from render_functions import RenderOrder
from item_functions import heal, seeker_bolt, flame_grenade, confuse, xpboost
from game_messages import Message
from random_utils import random_choice_from_dict, from_dungeon_level


class GameMap(Map):
    def __init__(self, width, height, dungeon_level=1):
        super().__init__(width, height)
        self.explored = [[False for y in range(height)] for x in range(width)]

        self.dungeon_level = dungeon_level


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other):
        # returns true if this rectangle intersects with another
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def create_room(game_map, room):
    # go through the tiles in the room and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map.walkable[x, y] = True
            game_map.transparent[x, y] = True


def create_h_tunnel(game_map, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def create_v_tunnel(game_map, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map.walkable[x, y] = True
        game_map.transparent[x, y] = True


def place_entities(room, entities, dungeon_level, colors):
    max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], dungeon_level)
    max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], dungeon_level)

    number_of_monsters = randint(0, max_monsters_per_room)
    number_of_items = randint(0, max_items_per_room)

    monster_chances = {"husk": 60,
                       "rusted_automaton": from_dungeon_level([[25, 3], [40, 5], [60, 7]], dungeon_level),
                       "kobold_bandit": from_dungeon_level([[10, 3], [20, 5], [25, 7]], dungeon_level)
                    }

    item_chances = {"health_drink": 40,
                    "wicked_blade": from_dungeon_level([[15, 3]], dungeon_level),
                    "battered_armor": from_dungeon_level([[15, 4]], dungeon_level),
                    "hp_ring": from_dungeon_level([[10, 5]], dungeon_level),
                    "seeker_orb": from_dungeon_level([[25, 4]], dungeon_level),
                    "flame_grenade": from_dungeon_level([[25, 6]], dungeon_level),
                    "scrambler": from_dungeon_level([[10, 2]], dungeon_level),
                    "pearl": 10}

    for i in range(number_of_monsters):
        # get a random location in the room
        x = randint(room.x1 + 1, room.x2 -1)
        y = randint(room.y1 + 1, room.y2 -1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            monster_choice = random_choice_from_dict(monster_chances)
            if monster_choice == "husk":
                fighter_component = Fighter(hp=15, defense=0, power=5, xp=50)
                ai_component = BasicMonster()
                # husk

                monster = Entity(x, y, "h", colors.get("dark_gray"), "husk", blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            elif monster_choice == "rusted_automaton":
                # rusted automaton
                fighter_component = Fighter(hp=20, defense=2, power=6, xp=75)
                ai_component = BasicMonster()

                monster = Entity(x, y, "a", colors.get("brass"), "rusted automaton", blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            elif monster_choice == "kobold_bandit":
                # kobold bandit
                fighter_component = Fighter(hp=35, defense=1, power=8, xp=100)
                ai_component = BasicMonster()

                monster = Entity(x, y, "b", colors.get("darker_flame"), "kobold bandit", blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

            entities.append(monster)

    for i in range(number_of_items):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            item_choice = random_choice_from_dict(item_chances)

            if item_choice == "health_drink":
                item_component = Item(use_function=heal, amount=50)
                item = Entity(x, y, "!", colors.get("violet"), "health drink", render_order=RenderOrder.ITEM,
                              item=item_component)
            elif item_choice == "wicked_blade":
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                item = Entity(x, y, ")", colors.get("darker_flame"), "wicked blade", equippable=equippable_component)
            elif item_choice == "battered_armor":
                equippable_component = Equippable(EquipmentSlots.BODY, defense_bonus=1)
                item = Entity(x, y, "T", colors.get("darker_orange"), "battered armor", equippable=equippable_component)
            elif item_choice == "hp_ring":
                equippable_component = Equippable(EquipmentSlots.RING, max_hp_bonus=30)
                item = Entity(x, y, "o", colors.get("copper"), "stalwart ring", equippable=equippable_component)
            elif item_choice == "flame_grenade":
                item_component = Item(use_function=flame_grenade, targeting=True, targeting_message=Message(
                    "Left-click where you'd like to throw the grenade, or right-click to cancel.",
                    colors.get("light_cyan")), damage=25, radius=3)
                item = Entity(x, y, ".", colors.get("red"), "flame grenade", render_order=RenderOrder.ITEM,
                              item=item_component)
            elif item_choice == "scrambler":
                item_component = Item(use_function=confuse, targeting=True, targeting_message=Message(
                    "Left-click an enemy you'd like to confuse, or right-click to cancel.", colors.get("light_cyan")))
                item = Entity(x, y, ".", colors.get("light_pink"), "scrambler", render_order=RenderOrder.ITEM,
                              item=item_component)
            elif item_choice == "pearl":
                item_component = Item(use_function=xpboost, amount=100)
                item = Entity(x, y, ".", colors.get("silver"), "pearl", render_order=RenderOrder.ITEM,
                              item=item_component)
            elif item_choice == "seeker_orb":
                item_component = Item(use_function=seeker_bolt, damage=30, maximum_range=5)
                item = Entity(x, y, ".", colors.get("sky"), "seeker orb", render_order=RenderOrder.ITEM,
                              item=item_component)

            entities.append(item)


def make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, colors):

    rooms = []
    num_rooms = 0

    center_of_last_room_x = None
    center_of_last_room_y = None

    for r in range(max_rooms):
        # random width and height
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        # random position within map boundaries
        x = randint(0, map_width - w - 1)
        y = randint(0, map_height - h - 1)

        # Rect class makes rectangles easier to use
        new_room = Rect(x, y, w, h)

        # check other rooms for intersections
        for other_room in rooms:
            if new_room.intersect(other_room):
                break

        else:
            create_room(game_map, new_room)

            # center coordinates of new room, for later
            (new_x, new_y) = new_room.center()

            center_of_last_room_x = new_x
            center_of_last_room_y = new_y

            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                # all rooms after the first are connected to the previous one by tunnel

                # center of previous room
                (prev_x, prev_y) = rooms[num_rooms -1].center()

                # flip a coin
                if randint(0, 1) == 1:
                    # horizontal then vertical
                    create_h_tunnel(game_map, prev_x, new_x, prev_y)
                    create_v_tunnel(game_map, prev_y, new_y, new_x)
                else:
                    # vertical then horizontal
                    create_v_tunnel(game_map, prev_y, new_y, prev_x)
                    create_h_tunnel(game_map, prev_x, new_x, new_y)

            place_entities(new_room, entities, game_map.dungeon_level, colors)

            rooms.append(new_room)
            num_rooms += 1

    stairs_component = Stairs(game_map.dungeon_level + 1)
    down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, ">", (255, 255, 255), "stairs",
                         render_order=RenderOrder.STAIRS, stairs=stairs_component)
    entities.append(down_stairs)


def next_floor(player, message_log, dungeon_level, constants):
    game_map = GameMap(constants["map_width"], constants["map_height"], dungeon_level)
    entities = [player]

    make_map(game_map, constants["max_rooms"], constants["room_min_size"], constants["room_max_size"],
             constants["map_width"], constants["map_height"], player, entities, constants["colors"])

    player.fighter.heal(player.fighter.max_hp // 2)

    message_log.add_message(Message("You feel invigorated at reaching new depths!",
                                    constants["colors"].get("light_violet")))

    return game_map, entities