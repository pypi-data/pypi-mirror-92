from enum import Enum


class AbstratEnum(Enum):
    def as_int(self) -> int:
        return self.value

class LogicalOperator(AbstratEnum):
    Equal = 1
    NotEqual = 2
    LessThan = 3
    LessThanOrEqual = 4
    GreaterThan = 5
    GreaterThanOrEqual = 6

class ConditionOperator(AbstratEnum):
    AND = 1
    OR = 2

class Unit(AbstratEnum):
    Price = 1
    Stock = 2
    Percentage = 3

class Side(AbstratEnum):
    Buy = 1
    Sell = 2

class AssetType(AbstratEnum):
    Equity = 1

class ChartType(AbstratEnum):
    OneMinute = 1
    FiveMinutes = 2
    FifteenMinutes = 3
    ThrityMinutes = 4
    OneDay = 5
