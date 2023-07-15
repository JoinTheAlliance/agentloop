import threading
import threading

from pynput import keyboard


def stop(loop_dict):
    """
    Function to handle stopping of the loop
    Args:
        loop_dict: a dictionary containing the stop event and the listener hich is created by the start function
    """

    listener = loop_dict["listener"]
    stop_event = loop_dict["stop_event"]
    stop_event.set()
    if listener is not None and listener.running:
        listener.stop()
    loop_dict["thread"].join(timeout=10)

def step(loop_dict):
    """
    Function to perform a single step in the loop

    Args:
        loop_dict: a dictionary containing the stop event and the listener hich is created by the start function

    This function does not return any value.
    """
    loop_dict["step_event"].set()


def start(steps, stepped=False):
    """
    Function to start the main loop

    Args:
        stepped: a boolean value that determines whether the loop should run in stepped mode or not. Defaults to False.

    Returns:
        thread, step_event: an instance of threading.Thread that's running the main loop and the event that's used to control stepping.
    """

    loop_dict = {
        "stop_event": threading.Event(),
        "step_event": threading.Event(),
        "started_event": threading.Event()
    }

    def on_press(key):
        if key == keyboard.Key.space:
            loop_dict["step_event"].set()
    
    listener = None
    if stepped:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    
    loop_dict["listener"] = listener

    thread = threading.Thread(target=loop, args=(steps, stepped, loop_dict))
    loop_dict["thread"] = thread

    thread.start()
    loop_dict["started_event"].wait()  # Wait here until loop is started

    return loop_dict


def loop(steps, stepped=False, loop_dict=None):
    """
    The main loop of the application, running the observe, orient, decide, act cycle until stop event is set

    Args:
        stepped: a boolean value that determines whether the loop should run in stepped mode or not
        stop_event: an instance of threading.Event that's used to control stopping of the loop
        step_event: an instance of threading.Event that's used to control stepping

    This function does not return any value.
    """
    if loop_dict is None:
        loop_dict = {
            "stop_event": threading.Event(),
            "step_event": threading.Event(),
            "started_event": threading.Event()
        }

    next_output = None
    loop_dict["started_event"].set()  # Indicate that the loop has started
    while not loop_dict["stop_event"].is_set():
        for step in steps:
            next_output = step(next_output)
            if stepped:
                while not loop_dict["step_event"].wait(
                    timeout=1
                ):  # Wait here until step_event is set
                    if loop_dict["stop_event"].is_set():  # Check if stop event has been set
                        break  # Break out of for loop
                if loop_dict["stop_event"].is_set():  # Check if stop event has been set
                    break  # Break out of for loop
                loop_dict["step_event"].clear()  # Clear the step_event
        if loop_dict["stop_event"].is_set():  # Check if stop event has been set
            break  # Break out of while loop