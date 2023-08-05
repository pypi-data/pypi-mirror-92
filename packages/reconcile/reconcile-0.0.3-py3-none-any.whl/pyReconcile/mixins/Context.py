# -*- coding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Collects two DeclarativeStates to represent the current and desired states to reconcile."""

from deepdiff import DeepDiff

from .DeclarativeState import DeclarativeStateMixin


class ContextMixin:
    """Collects two DeclarativeStates to represent the current and desired states to reconcile."""

    # Desired State and Current State MUST implement Declarative State
    def __init__(
        self,
        desired_state: DeclarativeStateMixin,
        current_state: DeclarativeStateMixin,
        **kwargs
    ):
        """Collects the desired_state and current_state for later use in diffing.

        Args:
            desired_state (DeclarativeStateMixin): The state a Plan should attempt to mutate the current_state into.
            current_state (DeclarativeStateMixin): The current state that needs to be reconciled to the desired one.
        """
        assert isinstance(desired_state, DeclarativeStateMixin)
        assert isinstance(current_state, DeclarativeStateMixin)
        self.desired_state = desired_state
        self.current_state = current_state
        super().__init__(**kwargs)

    def update_current_state(self, **kwargs):
        """Optional. Provide a way to update the current_state, like querying a REST API."""
        pass

    def update_desired_state(self, **kwargs):
        """Optional. Provide a way to update the desired_state, like querying a REST API."""
        pass

    def get_state_diff(self) -> DeepDiff:
        """Diffs the current state against the desired state.

        Returns:
            DeepDiff: The DeepDiff of the Current State against the Desired State.
        """
        return self.current_state.diff_declarative_state(self.desired_state)