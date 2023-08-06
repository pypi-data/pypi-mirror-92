from wrap_py import  wrap_base, settings
from wrap_engine import  sprite_of_type, sprite_type_factory, sprite_text
from wrap_py.wrap_sprite_utils import *
from wrap_py.wrap_sprite_type import *



def _register_sprite(sprite):
    id = wrap_base.sprite_id_manager.add_object(sprite)
    wrap_base.world.sprite_manager.add_image_sprite(sprite)
    return id

def remove_sprite(id):
    obj = wrap_base.sprite_id_manager.remove_by_id(id)
    if obj is not None:
        wrap_base.world.sprite_manager.remove_image_sprite(obj)

def sprite_exists(id):
    obj = wrap_base.sprite_id_manager.get_obj_id(id)
    return obj is not None


def add_sprite(sprite_type_name, x, y, visible=True, costume=None):
    # get sprite type
    if not wrap_base.sprite_type_manager.has_sprite_type_name(sprite_type_name):
        st = sprite_type_factory.Sprite_type_factory.create_sprite_type_from_file(sprite_type_name,
                                                                                  settings.SPRITE_TYPES_PATH)
        wrap_base.sprite_type_manager.add_sprite_type(st, sprite_type_name)

    sprite_type = wrap_base.sprite_type_manager.get_sprite_type_by_name(sprite_type_name)
    if not sprite_type:
        raise Exception(str(sprite_type_name) + " loading failed.")

    # make sprite of sprite type
    sprite = sprite_of_type.Sprite_of_type(sprite_type, x, y, costume, visible)

    return _register_sprite(sprite)

def add_text(x, y, text, visible = True, font_name="Arial", font_size=20,
                 bold=False, italic=False, underline=False,
                 text_color=(0, 0, 0),
                 back_color=None):
    sprite = sprite_text.Sprite_text(x, y, visible, text, font_name, font_size, bold, italic, underline, text_color, back_color)
    return _register_sprite(sprite)


def get_sprite_width(id):
    return _get_sprite_by_id(id).get_width_pix()


def get_sprite_height(id):
    return _get_sprite_by_id(id).get_height_pix()


def get_sprite_size(id):
    return _get_sprite_by_id(id).get_size_pix()


def set_sprite_original_size(id):
    _get_sprite_by_id(id).set_original_size()


def change_sprite_size(id, width, height):
    _get_sprite_by_id(id).change_size_pix(int(width), int(height))


def change_sprite_width(id, width):
    _get_sprite_by_id(id).change_width_pix(width)


def change_sprite_height(id, height):
    _get_sprite_by_id(id).change_height_pix(height)


def change_width_proportionally(id, width, from_modified=False):
    _get_sprite_by_id(id).change_width_pix_proportionally(width, from_modified)


def change_height_proportionally(id, height, from_modified=False):
    _get_sprite_by_id(id).change_height_pix_proportionally(height, from_modified)


def get_sprite_width_proc(id):
    return _get_sprite_by_id(id).get_width_proc()


def get_sprite_height_proc(id):
    return _get_sprite_by_id(id).get_height_proc()


def get_sprite_size_proc(id):
    return _get_sprite_by_id(id).get_size_proc()


def change_sprite_size_proc(id, width, height):
    _get_sprite_by_id(id).change_size_proc(int(width), int(height))


def change_sprite_width_proc(id, width):
    _get_sprite_by_id(id).change_width_proc(width)


def change_sprite_height_proc(id, height):
    _get_sprite_by_id(id).change_height_proc(height)


def change_sprite_size_by_proc(id, proc):
    _get_sprite_by_id(id).change_size_by_proc(proc)


def get_sprite_flipx_reverse(id):
    return _get_sprite_by_id(id).get_flipx_reverse()


def get_sprite_flipy_reverse(id):
    return _get_sprite_by_id(id).get_flipy_reverse()


def set_sprite_flipx_reverse(id, flipx):
    return _get_sprite_by_id(id).set_flipx_reverse(flipx)


def set_sprite_flipy_reverse(id, flipy):
    return _get_sprite_by_id(id).set_flipy_reverse(flipy)


def set_sprite_angle(id, angle):
    _get_sprite_by_id(id).set_angle_modification(angle)


def get_sprite_angle(id):
    return _get_sprite_by_id(id).get_angle_modification()


def get_sprite_final_angle(id):
    return _get_sprite_by_id(id).get_final_angle()


def move_sprite_to(id, x, y):
    return _get_sprite_by_id(id).move_sprite_to(x, y)


def move_sprite_by(id, dx, dy):
    _get_sprite_by_id(id).move_sprite_by(dx, dy)


def get_left(id):
    return _get_sprite_by_id(id).get_sprite_rect().left


def get_right(id):
    return _get_sprite_by_id(id).get_sprite_rect().right


def get_top(id):
    return _get_sprite_by_id(id).get_sprite_rect().top


def get_bottom(id):
    return _get_sprite_by_id(id).get_sprite_rect().bottom


def get_centerx(id):
    return _get_sprite_by_id(id).get_sprite_rect().centerx


def get_centery(id):
    return _get_sprite_by_id(id).get_sprite_rect().centery


def set_left_to(id, left):
    _get_sprite_by_id(id).set_left_to(left)


def set_right_to(id, right):
    _get_sprite_by_id(id).set_right_to(right)


def set_top_to(id, top):
    _get_sprite_by_id(id).set_top_to(top)


def set_bottom_to(id, bottom):
    _get_sprite_by_id(id).set_bottom_to(bottom)


def set_centerx_to(id, centerx):
    _get_sprite_by_id(id).set_centerx_to(centerx)


def set_centery_to(id, centery):
    _get_sprite_by_id(id).set_centery_to(centery)


def is_sprite_visible(id):
    return _get_sprite_by_id(id).get_visible()


def show_sprite(id):
    _get_sprite_by_id(id).set_visible(True)


def hide_sprite(id):
    _get_sprite_by_id(id).set_visible(False)


def move_sprite_at_angle(id, angle, distance):
    _get_sprite_by_id(id).move_sprite_at_angle(angle, distance)


def move_sprite_to_angle(id, distance):
    _get_sprite_by_id(id).move_sprite_to_angle(distance)


def move_sprite_to_point(id, x, y, distance):
    _get_sprite_by_id(id).move_sprite_to_point([x, y], distance)


def rotate_to_point(id, x, y):
    _get_sprite_by_id(id).rotate_to_point([x, y])


def sprites_collide(id1, id2):
    sp1 = _get_sprite_by_id(id1)
    sp2 = _get_sprite_by_id(id2)
    manager = wrap_base.get_sprite_manager()
    return manager.sprites_collide(sp1, sp2)


def sprites_collide_any(sprite_id, sprite_id_list):
    sprite_list = wrap_base.sprite_id_manager.get_obj_list_by_id_list(sprite_id_list)
    sprite = _get_sprite_by_id(sprite_id)

    manager = wrap_base.get_sprite_manager()
    collided_sprite = manager.sprite_collide_any(sprite, sprite_list)
    if collided_sprite is None: return None

    collided_sprite_id = wrap_base.sprite_id_manager.get_obj_id(collided_sprite)
    return collided_sprite_id

def sprites_collide_all(sprite_id, sprite_id_list):
    sprite_list = wrap_base.sprite_id_manager.get_obj_list_by_id_list(sprite_id_list)
    sprite = _get_sprite_by_id(sprite_id)

    manager = wrap_base.get_sprite_manager()
    collided_sprite_list = manager.sprite_collide_all(sprite, sprite_list)
    return wrap_base.sprite_id_manager.get_id_list_by_obj_list(collided_sprite_list)

