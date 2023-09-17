import arcade
import graphic_novel

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Graphic Novel Example"

def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = graphic_novel.GraphicNovel()
    game_view.characters = {"ME":arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png"),
                              "Man":arcade.Sprite(":resources:images/animated_characters/male_adventurer/maleAdventurer_idle.png")}
    game_view.setup("resource/dialog.json")
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()