"""
agentloop

A simple, lightweight loop for your agent. Start/stop, step-through, and more.
"""

__version__ = "0.1.0"
__author__ = "Autonomous Research Group"
__credits__ = "https://github.com/AutonomousResearchGroup/agentloop"

from .loop import start, step, stop, loop
from .input import step_with_input_key
from .context import create_default_context, create_context_builders

__all__ = [
    "start",
    "stop",
    "step",
    "loop",
    "step_with_input_key",
    "create_default_context",
    "create_context_builders",
]
