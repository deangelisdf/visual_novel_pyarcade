"""file: __init__.py
Unit Tests
"""
from unittest import mock

def get_window_dummy(w: int, h: int):
    # inspired from pyglet
    # A named function instead of a lambda for clarity in debugger views.
    def _get_dummy_shader_program(*args, **kwargs):
        return mock.MagicMock(width=w, height=h)
    return _get_dummy_shader_program
