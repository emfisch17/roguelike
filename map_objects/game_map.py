from random import randint
import tcod as libtcod

from components.ai import BasicMonster
from components.fighter import Fighter
from components.item import Item
from map_objects.rectangle import Rectangle
from map_objects.tile import Tile
from entity import Entity
from item_functions import heal, lightning_attack
from render_functions import RenderOrder


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width,
                 map_height, player, entities, max_monsters, max_items):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width/height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position within map boundary
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # Using Rectangle class makes the rooms easier to work with
            new_room = Rectangle(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # no intersections -> we can create the room

                # draw it on the map's tiles
                self.create_room(new_room)

                # center of new room
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # first room -> where player begins
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room via tunnel

                    # center of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # coin flip
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters, max_items)

                # add new room to the list of rooms
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        # make the tiles of the room passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters, max_items):
        # Get random number for monsters
        num_monsters = randint(0, max_monsters)
        num_items = randint(0, max_items)

        for i in range(num_monsters):
            # Pick a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 +1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_comp = Fighter(hp=10, defense=0, power=3)
                    ai_comp = BasicMonster()

                    monster = Entity(x, y, 'O', libtcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_comp, ai=ai_comp)
                else:
                    fighter_comp = Fighter(hp=16, defense=1, power=4)
                    ai_comp = BasicMonster()

                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_comp, ai=ai_comp)
                entities.append(monster)

        for i in range(num_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_chance = randint(0, 100)

                if item_chance < 70:
                    item_comp = Item(use_function=heal, amount=4)
                    item = Entity(x, y, '!', libtcod.violet, 'Healing Potion',
                                  render_order=RenderOrder.ITEM, item=item_comp)

                else:
                    item_comp = Item(use_function=lightning_attack, damage=20, max_range=5)
                    item = Entity(x, y, '#', libtcod.Color(255, 255, 0), 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_comp)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
