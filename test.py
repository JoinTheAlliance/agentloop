import time
import threading

from agentloop import (
    start,
    stop,
    step,
)

from pynput import keyboard

def step_one(options_dict):
    if options_dict is None:
        options_dict = {
            "step_one": 0,
            "step_two": 0
        }
    # increment step_one
    options_dict["step_one"] += 1
    print("step_one: ", options_dict["step_one"])
    return options_dict

def step_two(options_dict):
    # increment step_two
    options_dict["step_two"] += 1
    print("step_two: ", options_dict["step_two"])
    return options_dict

### Test for start function ###

def test_start():
    print("Starting test_start")
    loop_dict = start(steps=[step_one, step_two], stepped=False) 

    assert isinstance(loop_dict["thread"], threading.Thread)
    assert isinstance(loop_dict["step_event"], threading.Event)
    assert loop_dict["thread"].is_alive() == True
    stop(loop_dict)  # Stop the loop
    assert loop_dict["thread"].is_alive() == False


def test_start_stepped():
    print("Starting test_start_stepped")
    loop_dict = start(steps=[step_one, step_two], stepped=True)

    assert isinstance(loop_dict["thread"], threading.Thread)
    assert isinstance(loop_dict["step_event"], threading.Event)
    assert loop_dict["thread"].is_alive() == True
    for _ in range(5):
        step(loop_dict)
        # sleep 1 s
        time.sleep(.1)
    stop(loop_dict)  # Stop the loop
    assert loop_dict["thread"].is_alive() == False


if __name__ == "__main__":
    test_start_stepped()
    test_start()
    print("Tests successful")