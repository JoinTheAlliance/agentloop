import threading
import time

from agentloop import start, step, stop, pause, unpause


def step_one(options_dict, loop_data):
    if options_dict is None:
        options_dict = {"step_one": 0, "step_two": 0}
    # increment step_one
    options_dict["step_one"] += 1
    print("step_one: ", options_dict["step_one"])
    return options_dict


def step_two(options_dict):
    # increment step_two
    options_dict["step_two"] += 1
    print("step_two: ", options_dict["step_two"])
    return options_dict


def inner_loop(context):
    loop_data = start(steps=[step_one, step_two], paused=False)
    for _ in range(3):
        step(loop_data)
        # sleep 1 s
        time.sleep(0.1)
    stop(loop_data)  # Stop the loop
    return context


def test_inner_loop():
    print("Starting test_start")
    loop_data = start(steps=[step_one, inner_loop, step_two], paused=False)
    for _ in range(3):
        step(loop_data)
        # sleep 1 s
        time.sleep(0.1)
    assert isinstance(loop_data["thread"], threading.Thread)
    assert isinstance(loop_data["step_event"], threading.Event)
    assert loop_data["thread"].is_alive() is True
    stop(loop_data)  # Stop the loop
    assert loop_data["thread"].is_alive() is False


def test_start():
    print("Starting test_start")
    loop_data = start(steps=[step_one, step_two], paused=False)

    assert isinstance(loop_data["thread"], threading.Thread)
    assert isinstance(loop_data["step_event"], threading.Event)
    assert loop_data["thread"].is_alive() is True
    stop(loop_data)  # Stop the loop
    assert loop_data["thread"].is_alive() is False


def test_start_paused():
    print("Starting test_start_paused")
    loop_data = start(steps=[step_one, step_two], paused=True)

    assert isinstance(loop_data["thread"], threading.Thread)
    assert isinstance(loop_data["step_event"], threading.Event)
    assert loop_data["thread"].is_alive() is True
    for _ in range(5):
        step(loop_data)
        # sleep 1 s
        time.sleep(0.1)
    stop(loop_data)  # Stop the loop
    assert loop_data["thread"].is_alive() is False


def test_pause_unpause():
    print("Starting test_pause_unpause")

    shared_dict = {"paused": False}

    def check_pause_status(options_dict, loop_data):
        # Modify the shared_dict to reflect pause status
        shared_dict["paused"] = loop_data["pause_event"].is_set()
        return options_dict
    print("loop")
    loop_data = start(steps=[step_one, check_pause_status, step_two, check_pause_status], paused=False)
    print("loop2")
    assert isinstance(loop_data["thread"], threading.Thread)
    assert isinstance(loop_data["step_event"], threading.Event)
    assert loop_data["thread"].is_alive() is True
    print("assert")
    # Initially, we're not paused
    step(loop_data)
    time.sleep(0.1)
    assert shared_dict["paused"] == False

    # After pausing, we should be paused
    pause(loop_data)
    step(loop_data)
    shared_dict["paused"] = loop_data["pause_event"].is_set()
    time.sleep(1)
    assert shared_dict["paused"] == True

    # After unpausing, we should no longer be paused
    unpause(loop_data)
    step(loop_data)
    time.sleep(1)
    shared_dict["paused"] = loop_data["pause_event"].is_set()
    assert shared_dict["paused"] == False

    stop(loop_data)
    assert loop_data["thread"].is_alive() is False
