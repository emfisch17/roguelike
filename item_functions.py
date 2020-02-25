import tcod as libtcod

from messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are at full health already.', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('You drank the potion!', libtcod.green)})

    return results


def lightning_attack(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    max_range = kwargs.get('max_range')

    results = []

    target = None
    closest_dist = max_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_dist:
                target = entity
                closest_dist = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A lightning bolt hits {0}! It does {1} points of damage'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is within range'.libtcod.red)})

    return results
