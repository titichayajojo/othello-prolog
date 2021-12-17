try:
    import pygame
    from constant import *
    from game_file import *
    Game().run()

except ImportError as error:
    print('File: "main.py" cannot import :', error.name)
except NameError as error:
    print(error)
except IndentationError as error:
    print("Wrong indentation at :", error.filename,'\nLINE :', error.lineno)
except pygame.error as error:
    print("Pygame error.", error.args)
except CannotOpenFile as error:
    print("Cannot open file: " ,error.filename)
except Exception as e:
    print("Some error occurs.",e)
