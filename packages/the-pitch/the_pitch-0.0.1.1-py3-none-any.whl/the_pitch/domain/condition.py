from typing import List, Optional
from . import EntrySettings, AbstractRule, ConditionPayload
import numpy as np
from .enums import Side
import pandas as pd


class Condition(object):
    def __init__(self, settings: EntrySettings, rules: Optional[List[AbstractRule]] = []):
        self.settings = settings
        self.rules = rules

    @property
    def side(self) -> Side:
        return self.settings.side

    def is_valid(self, condition_payload: ConditionPayload, **kwargs) -> bool:
        parameters = dict(
            kwargs,
            condition_payload= condition_payload,
            settings=self.settings,
        )

        output = np.all([
            rule.is_valid(**parameters)
            for rule in self.rules
        ])

        if output:

            has_active_position = condition_payload.has_active_position

            if self.side == Side.Sell and not has_active_position:
                ## cant sell with no active positions
                return False

            if self.side == Side.Buy and has_active_position:
                ## no buying with positions still active
                return False

        return output
