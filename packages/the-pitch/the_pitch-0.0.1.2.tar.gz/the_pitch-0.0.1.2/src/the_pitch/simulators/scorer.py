from typing import List
from ..domain import Position
from decimal import Decimal


class Scorer(object):
    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    @staticmethod
    def score(operations: dict) -> dict:
        scores = {}
        for strategy_id in operations.keys():
            if strategy_id not in scores:
                scores[strategy_id] = {}

            for symbol in operations[strategy_id].keys():
                scores[strategy_id][symbol] = Scorer.score_positions(operations[strategy_id][symbol])

        return scores

    @staticmethod
    def score_positions(operations: List[Position]) -> Decimal:
        price = Decimal('0.0')

        if len(operations) == 0:
            return price

        grouped_operations = list(Scorer.chunks(operations, 2))
        if len(grouped_operations[-1]) == 1:
            ## the last position hasnt closed
            grouped_operations = grouped_operations[:-1]

        for row in grouped_operations:
            p1 = (row[1].quantity * row[1].purchase_price) ## should be larger,
            p2 = (row[0].quantity * row[0].purchase_price)
            price += (p1 - p2)

        return price
