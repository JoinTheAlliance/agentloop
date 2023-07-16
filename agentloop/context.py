from datetime import datetime
import importlib
import os
import sys


def create_context_builders(context_dir):
    """
    Build a context step function from the context builders in the given directory

    Returns:
    context: the context dictionary
    """
    context_dir = os.path.abspath(context_dir)
    sys.path.insert(0, context_dir)

    context_builders = []

    for filename in os.listdir(context_dir):
        if filename.endswith(".py"):
            module = importlib.import_module(f"{filename[:-3]}")

            if hasattr(module, "get_context_builders"):
                new_context_builders = module.get_context_builders()
                for context_builder in new_context_builders:
                    context_builders.append(context_builder)
    sys.path.remove(context_dir)

    def build_context(context={}):
        if context is None:
            context = {}

        for context_builder in context_builders:
            context = context_builder(context)
        return context

    return build_context


def create_default_context(context={}):
    """
    Create a default context object

    Args:
        context: the last context made by the loop. Defaults to None.

    Returns:
        context: a dictionary containing the current context
    """
    if context is None:
        context = {}
    context["current_time"] = datetime.now().strftime("%H:%M")
    context["current_date"] = datetime.now().strftime("%Y-%m-%d")
    context["platform"] = sys.platform
    context["cwd"] = os.getcwd()
    return context
