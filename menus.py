import tdl
import textwrap


def menu(con, root, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError("Cannot have a menu with more than 26 options.")

    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    height = len(options) + header_height

    # off-screen console to represent menu window
    window = tdl.Console(width, height)

    # print header
    window.draw_rect(0, 0, width, height, None, fg=(255, 255, 255), bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    y = header_height
    letter_index = ord("a")
    for option_text in options:
        text = "(" + chr(letter_index) + ") " + option_text
        window.draw_str(0, y, text, bg=None)
        y += 1
        letter_index += 1

    # blit the contents of "window" to root console
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - width // 2
    root.blit(window, x, y, width, height, 0, 0)


def inventory_menu(con, root, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each inventory item as an option
    if len(player.inventory.items) == 0:
        options = ["You're not carrying anything."]
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append("{0} (main hand)".format(item.name))
            elif player.equipment.body == item:
                options.append("{0} (worn)".format(item.name))
            elif player.equipment.ring == item:
                options.append("{0} (worn)".format(item.name))
            else:
                options.append(item.name)


    menu(con, root, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, root_console, background_image, screen_width, screen_height, colors):
    background_image.blit_2x(root_console, 0, 0)

    title = "TREASURE SHARK: THE SEA OF ISLANDS"
    center = (screen_width - len(title)) // 2
    root_console.draw_str(center, screen_height // 2 -4, title, bg=None, fg=colors.get("light_yellow"))

    title = "by Jacket"
    center = (screen_width - len(title)) // 2
    root_console.draw_str(center, screen_height - 2, title, bg=None, fg=colors.get("light_yellow"))

    menu(con, root_console, '', ["Start a new game", "Continue last game", "Quit"], 24, screen_width, screen_height)


def level_up_menu(con, root, header, player, menu_width, screen_width, screen_height):
    options = ["Endurance (+20 HP, from {0}".format(player.fighter.max_hp),
               "Strength (+1 attack, from {0}".format(player.fighter.power),
               "Agility (+1 defense, from {0}".format(player.fighter.defense)]

    menu(con, root, header, options, menu_width, screen_width, screen_height)


def character_screen(root_console, player, character_screen_width, character_screen_height, screen_width,
                     screen_height):
    window = tdl.Console(character_screen_width, character_screen_height)

    window.draw_rect(0, 0, character_screen_width, character_screen_height, None, fg=(255, 255, 255), bg=None)

    window.draw_str(0, 1, "Vital Statistics")
    window.draw_str(0, 2, "Level: {0}".format(player.level.current_level))
    window.draw_str(0, 3, "Experience: {0}".format(player.level.current_xp))
    window.draw_str(0, 4, "Next level in: {0}".format(player.level.experience_to_next_level))
    window.draw_str(0, 6, "Max HP: {0}".format(player.fighter.max_hp))
    window.draw_str(0, 7, "Attack: {0}".format(player.fighter.power))
    window.draw_str(0, 8, "Defense: {0}".format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    root_console.blit(window, x, y, character_screen_width, character_screen_height, 0, 0)


def message_box(con, root_console, header, width, screen_width, screen_height):
    menu(con, root_console, header, [], width, screen_width, screen_height)