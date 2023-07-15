# agentloop

A simple, lightweight loop for your agent. Start/stop, step-through, and more.

<img src="resources/image.jpg">

# Quickstart
```python
from agentloop import start, stop

def step_one(next_output):
    print("step_one")
    return next_output

def step_two(next_output):
    print("step_two")
    return next_output

# Run the loop
loop_dict = start(steps=[step_one, step_two]) 

# Stop the loop
stop(loop_dict)
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
def step_one(next_output): # next output None first run, then received from step_two
    print("step_one")
    return next_output # next output sent to step_two

def step_two(next_output): # next output received from step_one
    print("step_two")
    return next_output # next output sent to step_one

steps = [step_one, step_two]g
```

## Function `start`

```python
start(steps, stepped=False)
```

### Parameters
- `steps` : a list of functions that should be executed in the loop. Each function should accept a single argument and return a single value which will be passed as an argument to the next function. The first function will receive `None` as an argument.

- `stepped` (optional): a boolean value that determines whether the loop should run in stepped mode or not. Defaults to `False`.

### Returns
A dictionary containing
- `thread`: an instance of `threading.Thread` that's running the main loop.
- `stop_event`: an instance of `threading.Event` that's used to control stopping of the loop.
- `step_event`: an instance of `threading.Event` that's used to control stepping.
- `listener`: an instance of `keyboard.Listener` that's used to control stepping via spacebar.
- `started_event`: an instance of `threading.Event` that's set when the loop starts running.

---

## Function `stop`

```python
stop(loop_dict)
```

### Parameters
- `loop_dict`: a dictionary containing the `thread`, `stop_event`, `listener` which is returned by the `start` function.

### Returns
None

---

## Function `step`

```python
step(loop_dict)
```

### Parameters
- `loop_dict`: a dictionary containing the `thread`, `stop_event`, `step_event` which is returned by the `start` function.

### Returns
None

---

## Function `loop`

```python
loop(steps, stepped=False, loop_dict=None)
```

### Parameters
- `steps`: a list of functions that should be executed in the loop. Each function should accept a single argument and return a single value which will be passed as an argument to the next function. The first function will receive `None` as an argument.

- `stepped` (optional): a boolean value that determines whether the loop should run in stepped mode or not. Defaults to `False`.

- `loop_dict` (optional): a dictionary containing `stop_event` and `step_event` instances. If not provided, new events will be created.

### Returns
None

# Publishing

```bash
bash publish.sh --version=<version> --username=<pypi_username> --password=<pypi_password>
````

# Contributions Welcome

If you like this library and want to contribute in any way, please feel free to submit a PR and I will review it. Please note that the goal here is simplicity and accesibility, using common language and few dependencies.

<img src="resources/youcreatethefuture.jpg">
