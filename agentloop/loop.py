import threading


def start(steps, stepped=False):
    """
    Function to start the main loop

    Args:
        stepped: boolean - whether the loop should run one-step-at-a-time.
            Defaults to False.

    Returns:
        loop_data: a dictionary of loop data
    """

    loop_data = {
        "stop_event": threading.Event(),
        "step_event": threading.Event(),
        "started_event": threading.Event(),
    }

    thread = threading.Thread(target=loop, args=(steps, stepped, loop_data))
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


def loop(steps, stepped=False, loop_data=None):
    """
    Run the step array in a loop until stopped

    Args:
        steps: array of functions to be run in the loop
        stepped: boolean - whether the loop should run in stepped mode or not
        loop_data: loop data object, created by the start function

    This function does not return any value.
    """
    if loop_data is None:
        loop_data = {
            "stop_event": threading.Event(),
            "step_event": threading.Event(),
            "started_event": threading.Event(),
        }

    next_output = None
    loop_data["started_event"].set()  # Indicate that the loop has started
    while not loop_data["stop_event"].is_set():
        for step in steps:
            # check how many arguments step takes, 1 or 2?
            number_of_args = step.__code__.co_argcount
            if number_of_args == 1:
                next_output = step(next_output)
            elif number_of_args == 2:
                next_output = step(next_output, loop_data)
            else:
                raise ValueError(
                    "Step function must take 1 or 2 arguments"
                    "Valid arguments are next_output, loop_data (optional)"
                    "Found {} arguments".format(number_of_args)
                )
            if stepped:
                # Wait here until step_event is set
                while not loop_data["step_event"].wait(timeout=1):
                    if loop_data["stop_event"].is_set():
                        break
                if loop_data["stop_event"].is_set():
                    break
                loop_data["step_event"].clear()
        if loop_data["stop_event"].is_set():
            break


