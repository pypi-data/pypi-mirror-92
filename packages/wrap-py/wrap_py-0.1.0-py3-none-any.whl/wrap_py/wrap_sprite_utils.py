from wrap_py import wrap_base

__all__=["_get_sprite_by_id"]

def _get_sprite_by_id(id, check_type=None):
    sprite = wrap_base.sprite_id_manager.get_obj_by_id(id)
    if not sprite:
        raise Exception("No sprite with such id")  # TODO временный код

    if check_type is not None:
        if not isinstance(sprite, check_type):
            raise Exception("Sprite is not "+check_type.__name__)

    return sprite