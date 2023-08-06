from pyhartcmd import Action


class ExampleAction(Action):
    ACTION = "example"
    PARAM_NAME = "ACTION"

    def process_action(self, configuration):
        print("Hello I'm ExampleAction")
