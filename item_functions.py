from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    colors = args[1]
    amount = kwargs.get("amount")

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({"consumed": False, "message": Message("That might make you TOO healthy.",
                                                              colors.get("yellow"))})
    else:
        entity.fighter.heal(amount)
        results.append({"consumed": True, "message": Message("You feel healthier already!", colors.get("green"))})

    return results

def seeker_bolt(*args, **kwargs):
    caster = args[0]
    colors = args[1]
    entities = kwargs.get("entities")
    game_map = kwargs.get("game_map")
    damage = kwargs.get("damage")
    maximum_range = kwargs.get("maximum_range")

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and game_map.fov[entity.x, entity.y]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({"consumed": True, "target": target, "message": Message("A crackling beam sears from the orb toward the {0}, dealing {1} damage!".format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({"consumed": False, "target": None, "message": Message("No hostiles within range.", colors.get("red"))})

    return results