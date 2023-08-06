from wrap_py import  wrap_base as wb
import pygame

# general subscriber
def _register_event_handler(func, delay=None, count=0, pygame_event_type_filter_data=None, key_codes=None,
                            control_keys=None, mouse_buttons=None):
    # start event notification
    event_type_id = wb.event_generator.start_event_notification(
        delay=delay, count=count, force_new=True,
        event_filter=pygame_event_type_filter_data,
        key_codes=key_codes,
        control_keys=control_keys,
        mouse_buttons=mouse_buttons
    )

    subs = wb.message_broker.Subscriber(event_type_id, func)
    wb.broker.subscribe(subs)

    return event_type_id

def stop_listening(event_type_id):
    wb.event_generator.stop_event_notification(event_type_id)
    wb.broker.ubsubscribe_by_event_type_id(event_type_id)

def on_timeout(delay, count, func):
    return _register_event_handler(
        func=func,
        delay=delay,
        count=count
    )

def on_key_down(key, func):
    return _register_event_handler(
        func=func,
        pygame_event_type_filter_data={
            'type': pygame.KEYDOWN,
            'key': key
        })

def on_key_pressed(keys, func, delay=100, control_keys=None):
    #must be iterable
    if not hasattr(keys, "__iter__"):
        keys = [keys]

    # must be iterable
    if control_keys is not None and \
            not hasattr(control_keys, "__iter__"):
        control_keys = [control_keys]

    return _register_event_handler(
        func=func,
        delay=delay,
        key_codes=keys,
        control_keys=control_keys
    )

def on_mouse_pressed(buttons, func, delay=100, control_keys=None):
    # must be iterable
    if not hasattr(buttons, "__iter__"):
        buttons = [buttons]

    # must be iterable
    if control_keys is not None and \
            not hasattr(control_keys, "__iter__"):
        control_keys = [control_keys]

    return _register_event_handler(
        func=func,
        delay=delay,
        mouse_buttons=buttons,
        control_keys=control_keys
    )

_on_quit_event_id = None
def on_close_callback(**kwargs):
    exit()
def on_close(func):
    global _on_quit_event_id

    if _on_quit_event_id is not None:
        stop_listening(_on_quit_event_id)

    _on_quit_event_id = _register_event_handler(
        func=func,
        pygame_event_type_filter_data={'type': pygame.QUIT}
    )
    return _on_quit_event_id

on_close(on_close_callback)
