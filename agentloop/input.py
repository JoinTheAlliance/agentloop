def step_with_input_key(loop_data, input_key=None):
    """
    Listen for a specified key press, and when detected, step the loop

    Args:
        loop_data: loop data object, created by the start function
        input_key: The keyboard key which the listener will react to
            Defaults to keyboard.Key.space

    Returns:
        loop_data: The updated loop dictionary with the newly created listener
    """
    keyboard = None
    try:
        from pynput import keyboard as _keyboard
        keyboard = _keyboard
    except ImportError:
        raise ImportError(
            "pynput not installed. Please install it with `pip install pynput`"
        )

    if input_key is None:
        input_key = keyboard.Key.space

    def on_press(key):
        if key == input_key:
            loop_data["step_event"].set()

    listener = None
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    loop_data["listener"] = listener
    return loop_data
