# -*- coding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Action base representing the smallest procedures for a Plan to carry out."""

from .Context import ContextMixin


class ActionMixin:
    """Abstract base representing the smallest procedures for a Plan to carry out.

    Actions are assembled by Plans and executed by Schedulers.
    Plans shoudl architect the overall procedure, but Actions MAY act as flowcontrol during plan execution.

    See "do".
    """

    def __init__(self, action_name: str, **kwargs):
        """Initialize an Action.

        Provide additional arguments in your constructor to configure your Actions.

        Args:
            action_name (str): A name uniquely identifying this action. Useful for logging.
            **kwargs: Provide additional arguments when implementing your Actions' constructors for configuration.

        """
        self.action_name = action_name
        super().__init__(**kwargs)

    # Must return another LIST of Actions or nothing
    # Must modify Context to reflect the actions taken
    def do(self, context: ContextMixin):
        """Do the action.

        Actions are assembled by Plans and executed by Schedulers. This is the entry hook into an Action.
        Actions MAY return a list of Actions to be executed following their own execution.
        Plans should architect the overall procedure, but this provides plan-runtime flow control.

        Args:
            context (ContextMixin): "do" references and may mutate Context, one step at a time.

        Raises:
            NotImplementedError: Must be implemented by child classes.

        Returns:
            list(ActionMixin): Optionally return a list of actions to be preformed after this one.

        """
        raise NotImplementedError

    def string(self):
        """Return a string representation of this Action for logging.

        Should state the intent of the action preformed.

        Returns:
            str: A string representation of this Action suitible for logging. Defaults to self.action_name.

        """
        return "{}".format(self.action_name)


if __name__ == "__main__":

    class __TestAction(ActionMixin):
        """Action for unit tests.

        Todo:
            Write better tests now that Contexts are finished.
        """

        def __init__(self, some: str, data: str, **kwargs):
            """Construct a Test Action with some member variables.

            Args:
                some (str): foo data
                data (str): bar data
            """
            self.some = some
            self.data = data
            super().__init__(**kwargs)

        def do(self, context):
            """Showcases actions' flowcontrol ability.

            Args:
                context: just a string for comparison.

            Returns:
                list(ActionMixin): Might return another TestAction.
            """
            # Do something with the context, in line with the name of the Action
            print(context == "TestVal")
            if context == "TestVal":
                return [__TestAction("Other", "Data", action_name="Recursive Action")]

    TA = __TestAction("Some", "Data", action_name="Test Context against TestVal")
    print(TA.do("TestVal")[0].do("TestVal")[0].do("Not TestVal"))
