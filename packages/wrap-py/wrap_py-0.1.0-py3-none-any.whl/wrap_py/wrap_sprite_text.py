from wrap_py.wrap_sprite_utils import *
from wrap_engine.sprite_text import Sprite_text

def is_sprite_text(id):
    sprite = _get_sprite_by_id(id)
    return isinstance(sprite, Sprite_text)

def get_font_name(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_font_name()


def set_font_name(id, name):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_data(font_name=name)


def get_font_size(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_font_size()


def set_font_size(id, size):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_data(font_size=size)


def get_font_bold(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_font_bold()


def set_font_bold(id, bold):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_data(bold=bold)


def get_font_italic(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_font_italic()

def set_font_italic(id, italic):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_data(italic=italic)

def get_font_underline(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_font_underline()

def set_font_underline(id, underline):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_data(underline=underline)

def get_text(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_text()

def set_text(id, text):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_data(text=text)

def get_text_color(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_text_color()

def set_text_color(id, text_color):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_data(text_color=text_color)

def get_back_color(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_back_color()

def set_back_color(id, back_color):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_back_color(back_color)

def get_pos(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_pos()

def set_pos(id, pos):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_pos(pos)


def get_angle(id):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.get_angle()

def set_angle(id, pos):
    sprite = _get_sprite_by_id(id, Sprite_text)
    return sprite.change_angle(pos)