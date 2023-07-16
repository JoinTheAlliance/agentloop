import threading
import time

from agentloop import start, step, stop


def step_one(options_dict, loop_data):
    if options_dict is None:
        options_dict = {"step_one": 0, "step_two": 0}
    # increment step_one
    options_dict["step_one"] += 1
    print("step_one: ", options_dict["step_one"])
    return options_dict


def step_two(options_dict, loop_data):
    # increment step_two
    options_dict["step_two"] += 1
    print("step_two: ", options_dict["step_two"])
    return options_dict

def inner_loop(context):
    loop_data = start(steps=[step_one, step_two], stepped=False)
    for _ in range(3):
        step(loop_data)
        # sleep 1 s
        time.sleep(0.1)
    stop(loop_data)  # Stop the loop
    return context

def test_inner_loop():
    print("Starting test_start")
    loop_data = start(steps=[step_one, inner_loop, step_two], stepped=False)
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
    loop_data = start(steps=[step_one, step_two], stepped=False)

    assert isinstance(loop_data["thread"], threading.Thread)
    assert isinstance(loop_data["step_event"], threading.Event)
    assert loop_data["thread"].is_alive() is True
    stop(loop_data)  # Stop the loop
    assert loop_data["thread"].is_alive() is False


def test_start_stepped():
    print("Starting test_start_stepped")
    loop_data = start(steps=[step_one, step_two], stepped=True)

    assert isinstance(loop_data["thread"], threading.Thread)
    assert isinstance(loop_data["step_event"], threading.Event)
    assert loop_data["thread"].is_alive() is True
    for _ in range(5):
        step(loop_data)
        # sleep 1 s
        time.sleep(0.1)
    stop(loop_data)  # Stop the loop
    assert loop_data["thread"].is_alive() is False
