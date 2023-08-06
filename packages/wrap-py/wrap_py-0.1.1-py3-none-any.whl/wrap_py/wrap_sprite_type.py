from wrap_py.wrap_sprite_utils import *

def change_sprite_costume(id, costume_name, save_moving_angle=False, apply_proc_size=True):
    sprite = _get_sprite_by_id(id)
    if hasattr(sprite, "set_costume"):
        sprite.set_costume(costume_name, save_moving_angle, apply_proc_size)


def set_next_costume(id, save_moving_angle=False, apply_proc_size=True):
    sprite = _get_sprite_by_id(id)
    if hasattr(sprite, "set_costume_by_offset"):
        sprite.set_costume_by_offset(1, save_moving_angle, apply_proc_size)


def set_previous_costume(id, save_moving_angle=False, apply_proc_size=True):
    sprite = _get_sprite_by_id(id)
    if hasattr(sprite, "set_costume_by_offset"):
        sprite.set_costume_by_offset(-1, save_moving_angle, apply_proc_size)


def get_sprite_costume(id):
    sprite = _get_sprite_by_id(id)
    if hasattr(sprite, "get_sprite_costume"):
        return sprite.get_sprite_costume()