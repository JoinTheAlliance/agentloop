# agentloop <a href="https://discord.gg/qetWd7J9De"><img style="float: right" src="https://dcbadge.vercel.app/api/server/qetWd7J9De" alt=""></a>

A simple, lightweight loop for your agent. Start/stop, step-through, and more.

<img src="resources/image.jpg">

[![Lint and Test](https://github.com/AutonomousResearchGroup/agentloop/actions/workflows/test.yml/badge.svg)](https://github.com/AutonomousResearchGroup/agentloop/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/agentloop.svg)](https://badge.fury.io/py/agentloop)

# Quickstart

```python
from agentloop import start, stop

def step_one(next_output, loop_data):
    print("step_one")
    return next_output

def step_two(next_output, loop_data):
    print("step_two")
    return next_output

# Run the loop
loop_data = start(steps=[step_one, step_two])

# Stop the loop
stop(loop_data)
```

# Installation

```bash
pip install agentloop
```

# Usage

This package provides a set of functions to perform a stepped or continuous loop of operations in a separate thread. This can be used for various purposes like running a continuous process that can be controlled from the outside, a debugging tool for a cycle of operations, etc.

## Steps

Each step must take in input from the last step and return output for the next step. The first step will receive None as input, and this will need to be handled. You can either start with an initialization step that returns the initial input, or you can check for None in the first step and return the initial input if it is None.

Example steps:

```python
def step_one(next_output, loop_data): # next output None first run, then received from step_two
    print("step_one")
    return next_output # next output sent to step_two

def step_two(next_output, loop_data): # next output received from step_one
    print("step_two")
    return next_output # next output sent to step_one

steps = [step_one, step_two]
```

## Function `start`

```python
start(steps, stepped=False)
```

### Description

Starts the main loop in a separate thread. This loop will run the steps given, in a continuous or stepped manner.

### Parameters

- `steps` : a list of functions that should be executed in the loop. Each function should accept a single argument and return a single value which will be passed as an argument to the next function. The first function will receive `None` as an argument.

- `stepped` (optional): a boolean value that determines whether the loop should run in stepped mode or not. Defaults to `False`.

### Returns

A dictionary containing

- `stop_event`: an instance of `threading.Event` that's used to control stopping of the loop.
- `step_event`: an instance of `threading.Event` that's used to control stepping.
- `started_event`: an instance of `threading.Event` that's set when the loop starts running.
- `thread`: an instance of `threading.Thread` that's running the main loop.

---

## Function `stop`

```python
stop(loop_data)
```

### Description

Handles stopping of the loop.

### Parameters

- `loop_data`: a dictionary containing the `stop_event` and `thread` which is returned by the `start` function.

### Returns

None

---

## Function `step`

```python
step(loop_data)
```

### Description

Performs a single step in the loop.

### Parameters

- `loop_data`: a dictionary containing the `step_event` which is returned by the `start` function.

### Returns

None

---

## Function `loop`

```python
loop(steps, stepped=False, loop_data=None)
```

### Description

Runs the step array in a loop until stopped.

### Parameters

- `steps`: a list of functions that should be executed in the loop. Each function should accept a single argument and return a single value which will be passed as an argument to the next function. The first function will receive `None` as an argument.

- `stepped` (optional): a boolean value that determines whether the loop should run in stepped mode or not. Defaults to `False`.

- `loop_data` (optional): a dictionary containing `stop_event` and `step_event` instances. If not provided, new events will be created.

### Returns

None

## Function `use_keyboard`

```python
use_keyboard(loop_data, input_key=keyboard.Key.space)
```

### Description

Creates a keyboard listener and attaches it to the provided loop data object. This listener listens for a specified key press, and when detected, steps the loop (sets the 'step_event').

### Parameters

- `loop_data`: A loop data object, which is typically created by the `start` function.

- `input_key` (optional): The keyboard key that the listener will react to. Defaults to `keyboard.Key.space`.

### Returns

Returns the updated loop dictionary with the newly created keyboard listener added to it.
Note: Pass the updated dictionary to the stop function to also stop the keyboard listener

Defaults to Spacebar

### Example

```python
loop_data = {
    "stop_event": threading.Event(),
    "step_event": threading.Event(),
    "started_event": threading.Event(),
    "thread": None,
}

updated_loop_dict = use_keyboard(loop_data, input_key)
```

# Testing
```
pytest test.py
```

# Publishing

```bash
bash publish.sh --version=<version> --username=<pypi_username> --password=<pypi_password>
```

# Contributions Welcome

If you like this library and want to contribute in any way, please feel free to submit a PR and I will review it. Please note that the goal here is simplicity and accesibility, using common language and few dependencies.

<img src="resources/youcreatethefuture.jpg">
