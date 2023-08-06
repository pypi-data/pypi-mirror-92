from wrap_py import  wrap_base

def create_world(width, height):
    wrap_base.world.create_world(width, height)

def change_world(width, height):
    wrap_base.world.change_world(width, height)

def set_world_background_color(color):
    wrap_base.world.set_world_background_color(color)

def set_world_background_image(path_to_file, fill=False):
    wrap_base.world.set_world_background_image(path_to_file, fill)