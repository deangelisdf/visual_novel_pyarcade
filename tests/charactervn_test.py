"""Unit test graphic novel view
author: domenico francesco de angelis"""
import sys
import os
import unittest
import arcade.application

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)

import tests # noqa: E402
import graphic_novel # noqa: E402
from graphic_novel.character_vn import CharacterVN # noqa: E402

arcade.get_window = tests.get_window_dummy(300,300)
gn_view = graphic_novel.GraphicNovel()
class gn_testing(unittest.TestCase):
    def test_setter(self):
        c_test = CharacterVN("test")
        texture:arcade.Texture = arcade.texture.make_circle_texture(
                                30, arcade.color.AERO_BLUE)
        sprite_test = arcade.Sprite(texture=texture)
        c_test.sprites = {"idle":sprite_test}
        c_test.state = "x"
        self.assertTrue("idle" == c_test.state)
        self.assertTrue(c_test.height == sprite_test.height)
        self.assertTrue(c_test.width == sprite_test.width)
        c_test.bottom = 10
        self.assertTrue(c_test.bottom == 10)
        self.assertTrue(c_test.sprites["idle"].bottom == 10)
        c_test.right = 10
        self.assertTrue(c_test.right == 10)
        self.assertTrue(c_test.sprites["idle"].right == 10)
        c_test.left = 10
        self.assertTrue(c_test.left == 10)
        self.assertTrue(c_test.sprites["idle"].left == 10)
        c_test.top = 10
        self.assertTrue(c_test.sprites["idle"].top == 10)
        self.assertTrue(c_test.top == 10)

if __name__ == "__main__":
    unittest.main()
