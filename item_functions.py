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