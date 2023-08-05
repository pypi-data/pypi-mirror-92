"""
Tests.
"""

import sys

sys.path.insert(0, '../../')

import pygame
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))


# noinspection PyMissingOrEmptyDocstring,PyUnusedLocal
def set_difficulty(value, difficulty):
    pass


# noinspection PyMissingOrEmptyDocstring
def start_the_game():
    pass


menu = pygame_menu.Menu(300,
                        400,
                        'Welcome',
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add_text_input('Name :', default='John Doe')
menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)],
                  onchange=set_difficulty)
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)
