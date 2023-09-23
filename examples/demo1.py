import os
import sys
import arcade
from pyglet.math import Vec2
src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, src_path)
import graphic_novel # noqa: E402

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Graphic Novel Example"

PATH_C1_NORMAL=":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
PATH_C1_HAPPY =":resources:images/animated_characters/female_adventurer/femaleAdventurer_jump.png"

def end_game(context: graphic_novel.GraphicNovel):
    """function used at the end of dialog"""
    print("end. last dialog:", context.history_labels[-1])

def quest_ev(context: graphic_novel.GraphicNovel):
    if int(context.input_text.text) == 10:
        context.jmp_next_dialog("ok_resp")
    else:
        context.jmp_next_dialog("bad_resp")

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = graphic_novel.GraphicNovel()
    res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource")
    arcade.resources.add_resource_handle("res", res_path)
    game_view.characters = {"Emma":{"idle" :arcade.Sprite(PATH_C1_NORMAL),
                                    "happy":arcade.Sprite(PATH_C1_HAPPY)}
                            }
    game_view.add_event("quest_ev", quest_ev)
    game_view.setup(":res:demo.json")
    game_view.text_area.delay_typing = 0
    game_view.input_handler.change_key("Hide gui", arcade.key.H)
    game_view.input_handler.change_key("Next Dialog", arcade.key.RIGHT)
    game_view.on_ended = end_game
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()
