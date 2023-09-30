from second_source import *
import os.path
print("\033[38;5;108m Welcome to 'X-O' Game \033[0;0m")
if os.path.exists("Game.txt"):
      continue_game()
else:
      choose_mode_game()
