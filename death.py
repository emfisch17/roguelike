import tcod as libtcod

from game_states import GameStates

def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return "Game Over", GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = 'You killed {0}!'.format(monster.name.capitalize())

    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = monster.name + "'s remains"

    return death_message

