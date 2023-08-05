# -*- coding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""The core representation of state for reconciliation.

Makes use of DeepDiff to provide a solid representation of the differences
that need to be reconciled between two instances of DeclarativeStates.

Some DeepDiff kwargs can be passed through the constructor for
the instance's diffing against another instance. This is not symmetric.
"""

from deepdiff import DeepDiff


class DeclarativeStateMixin(object):
    """The core representation of state for reconciliation."""

    def __init__(
        self,
        declarative_state_data,
        declarative_state_ignore_order=True,
        declarative_state_report_repetition=False,
        **kwargs
    ):
        """Construct a DeclarativeState around any data supported by DeepDiff.

        DeepDiff's kwargs provided here are used in this instance's diff_declarative_state call.

        Args:
            declarative_state_data: Data representing state. Must be supported by DeepDiff.
            declarative_state_ignore_order (bool, optional): See DeepDiff's docs for details. Defaults to True.
            declarative_state_report_repetition (bool, optional): See DeepDiff's docs for details. Defaults to False.
        """
        self.state = declarative_state_data
        self.__ignore_order = declarative_state_ignore_order
        self.__report_repetition = declarative_state_report_repetition
        self.__verbose_level = 2
        super().__init__(**kwargs)

    @property
    def state(self):
        """Access the internal State data. Useful for fetching data for use by Actions."""
        return self.__state

    @state.setter
    def state(self, val):
        self.__state = val

    def diff_declarative_state(self, other) -> DeepDiff:
        """Run DeepDiff against another DeclarativeState.

        Used when comparing the Desired State against the Current State in a Context.
        Uses this instance's DeepDiff kwargs from this instance's constructor.

        Args:
            other (DeclarativeStateMixin): The other DeclarativeState to diff against.

        Returns:
            DeepDiff: The DeepDiff between this and other.
        """
        return DeepDiff(
            self.state,
            other.state,
            ignore_order=self.__ignore_order,
            report_repetition=self.__report_repetition,
            verbose_level=self.__verbose_level,
        )


if __name__ == "__main__":
    print("Testing DeclarativeState Mixin")
    t1 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 2, 3]}, 5: 5}
    t2 = {1: 1, 2: 2, 3: 3, 4: {"a": "hello", "b": [1, 3, 2, 3]}}
    print(t1)
    print(t2)

    class __Test(DeclarativeStateMixin):
        def __init__(self, name, *args, **kwargs):
            super().__init__(**kwargs)
            self.name = name

    ignore_order = True
    report_repetition = True
    a1 = __Test(
        "Name is a1", declarative_state_data=t1
    )  # , declarative_state_ignore_order=ignore_order, declarative_state_report_repetition=report_repetition)
    a2 = __Test(
        "Name is a2", declarative_state_data=t2
    )  # , declarative_state_ignore_order=ignore_order, declarative_state_report_repetition=report_repetition)
    print(a1.diff_declarative_state(a2))
    d = a1.diff_declarative_state(a2)
    b1 = __Test(
        "Name is b1",
        declarative_state_data=[1, 2, 3],
        declarative_state_ignore_order=False,
        declarative_state_report_repetition=True,
    )
    b2 = __Test(
        "Name is b2",
        declarative_state_data=[1, 3, 3, 4],
        declarative_state_ignore_order=False,
        declarative_state_report_repetition=True,
    )
    b3 = __Test(
        "Name is b3",
        declarative_state_data=[1, 3],
        declarative_state_ignore_order=False,
        declarative_state_report_repetition=True,
    )
    b4 = __Test(
        "Name is b4",
        declarative_state_data=[1, 2, 3],
        declarative_state_ignore_order=False,
        declarative_state_report_repetition=True,
    )
    print(b1.diff_declarative_state(b2))
    print(b1.state)
    b1.state[1] = 3
    b1.state.append(4)
    print(b1.state)
    print(b1.diff_declarative_state(b2))
    print(b4.diff_declarative_state(b3))
