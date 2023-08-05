from decimal import Decimal


def decimal_from_value(value):
    return Decimal(value)

def decimal_from_float(value: float):
    return Decimal(str(round(value, 2)))