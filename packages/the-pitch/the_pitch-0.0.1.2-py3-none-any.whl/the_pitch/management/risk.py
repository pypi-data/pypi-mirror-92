from decimal import Decimal


def get_quantity(total_capital: Decimal, risk: Decimal, expected_stop_loss_per_share: Decimal):
    return (total_capital * risk) / expected_stop_loss_per_share

def pe(stock_price: Decimal, eps: Decimal):
    return stock_price / eps

def short_interest(company_float: int, reported_short: int):
    ## level of sentiment, who thinks the stock is overvalued
    return reported_short / company_float