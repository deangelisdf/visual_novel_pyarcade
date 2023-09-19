"""Unit test graphic novel view
author: domenico francesco de angelis"""
import sys
import os
import unittest

src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, src_path)

#import graphic_novel # noqa: E402

class gn_testing(unittest.TestCase):
    def test_setup(self):
        pass

if __name__ == "__main__":
    unittest.main()
