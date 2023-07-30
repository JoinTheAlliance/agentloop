import threading


def start(steps, paused=False):
    """
    Function to start the main loop

    Args:
        paused: boolean - whether the loop should run automatically. If paused can be stepped one-step-at-a-time.
            Defaults to False.

    Returns:
        loop_data: a dictionary of loop data
    """

    loop_data = {
        "stop_event": threading.Event(),
        "step_event": threading.Event(),
        "started_event": threading.Event(),
        "pause_event": threading.Event(),
    }

    if paused:
        loop_data["pause_event"].set()

    thread = threading.Thread(target=loop, args=(steps, loop_data))
    loop_data["thread"] = thread

    thread.start()
    loop_data["started_event"].wait()  # Wait here until loop is started

    return loop_data


def stop(loop_data):
    """
    Function to handle stopping of the loop
        loop_data: a dictionary containing threading events related to the loop
            (You should pass in the object created by the start function)
    """

    listener = loop_data.get("listener", None)
    stop_event = loop_data["stop_event"]
    stop_event.set()
    if listener is not None and listener.running:
        listener.stop()
    try:
        loop_data["thread"].join(timeout=10)
    except RuntimeError:
        pass


def step(loop_data):
    """
    Function to perform a single step in the loop

    Args:
        loop_data: loop data object, created by the start function

    This function does not return any value.
    """
    loop_data["step_event"].set()


def pause(loop_data):
    """
    Function to pause the loop

    Args:
        loop_data: loop data object, created by the start function

    This function does not return any value.
    """
    loop_data["pause_event"].set()


def unpause(loop_data):
    """
    Function to unpause the loop

    Args:
        loop_data: loop data object, created by the start function

    This function does not return any value.
    """
    loop_data["pause_event"].clear()


def loop(steps, loop_data):
    """
    Run the step array in a loop until stopped

    Args:
        steps: array of functions to be run in the loop
        paused: boolean - whether the loop should run start up paused (can be stepped) or running
        loop_data: loop data object, created by the start function

    This function does not return any value.
    """
    next_output = None
    loop_data["started_event"].set()  # Indicate that the loop has started
    while not loop_data["stop_event"].is_set():
        for step in steps:
            number_of_args = step.__code__.co_argcount
            if number_of_args == 1:
                next_output = step(next_output)
            elif number_of_args == 2:
                next_output = step(next_output, loop_data)
            else:
                raise ValueError(
                    "Step function must take 1 or 2 arguments. "
                    "Valid arguments are next_output, loop_data (optional). "
                    "Found {} arguments".format(number_of_args)
                )

            while loop_data["pause_event"].is_set():
                print("Loop paused")
                if loop_data["stop_event"].wait(timeout=1):
                    return
            if loop_data["step_event"].wait(timeout=1):
                loop_data["step_event"].clear()
        if loop_data["stop_event"].is_set():
            break

