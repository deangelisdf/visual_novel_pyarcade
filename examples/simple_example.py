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

PATH_CHARACTER_1=":resources:images/animated_characters/female_person/femalePerson_idle.png"
PATH_CHARACTER_2=":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png"

def event1(gn: graphic_novel.GraphicNovel) -> int:
    print("Quest added", gn.characters.keys())
    crt_filter = arcade.experimental.CRTFilter(SCREEN_WIDTH, SCREEN_HEIGHT,
                                                resolution_down_scale=1.0,
                                                hard_scan=-4.0,
                                                hard_pix=-1.0,
                                                display_warp=Vec2(1.0/32.0, 1.0/24.0),
                                                mask_dark=0.3,
                                                mask_light=1.0)
    gn.add_filter_video(crt_filter)
    gn.set_color_text((255,0,0,255))
    return 1

def end_game(context: graphic_novel.GraphicNovel):
    """function used at the end of dialog"""
    print("end. last dialog:", context.history_labels[-1])

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = graphic_novel.GraphicNovel()
    res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource")
    arcade.resources.add_resource_handle("res", res_path)
    game_view.characters = {"ME":arcade.Sprite(PATH_CHARACTER_1),
                            "Man":arcade.Sprite(PATH_CHARACTER_2)}
    game_view.setup(":res:dialog.json")
    game_view.add_event("event1", event1)
    game_view.on_ended = end_game
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()
