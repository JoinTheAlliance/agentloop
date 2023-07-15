"""
agentloop

A simple, lightweight loop for your agent. Start/stop, step-through, and more.
"""

__version__ = "0.1.0"
__author__ = "Autonomous Research Group"
__credits__ = "https://github.com/AutonomousResearchGroup/agentloop"

from .main import (
    start,
    stop,
    step,
)

__all__ = [
    "start",
    "stop",
    "step",
]
