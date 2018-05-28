from numpy.random import choice


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    decimal_chances = [chance / sum(chances) for chance in chances]

    return choice(choices, p=decimal_chances)