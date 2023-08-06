from argparse import ArgumentParser

from pyhartcmd.actions.example_action.example_action import ExampleAction
from pyhartcmd.actions.version import ShowVersion
from pyhartcmd.framework.messages import Messages


class ActionDispatcher:
    ACTION_HANDLERS = [ExampleAction, ShowVersion]

    def __init__(self):
        self.parser = ArgumentParser()
        subparsers = self.parser.add_subparsers()
        self.action_handlers = {action_handler.ACTION: action_handler(subparsers) for action_handler in
                                self.ACTION_HANDLERS}

    def process_application(self):
        configuration = self.parser.parse_args()
        try:
            self.action_handlers[configuration.ACTION].process_action(configuration)
        except AttributeError:
            Messages.clean("hart ::")
