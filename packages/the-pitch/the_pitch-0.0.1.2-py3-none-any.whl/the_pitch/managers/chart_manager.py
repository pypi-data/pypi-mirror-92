from datetime import datetime, timedelta
from typing import Tuple
from pytz import timezone
from ..domain import ChartType


class ChartManager(object):
    def __init__(self, chart_type: ChartType) -> None:
        self.chart_type = chart_type

    def get_timedelta(self):
        if self.chart_type == ChartType.OneMinute:
            return timedelta(minutes=1)

        if self.chart_type == ChartType.FiveMinutes:
            return timedelta(minutes=5)

        if self.chart_type == ChartType.FifteenMinutes:
            return timedelta(minutes=15)

        if self.chart_type == ChartType.ThrityMinutes:
            return timedelta(minutes=30)

        if self.chart_type == ChartType.OneDay:
            return timedelta(days=1)

        raise ValueError(f'{self.chart_type.name} not implemented.')

    def get_next_expected_bar(self, last_bar_timestamp: datetime) -> datetime:
        delta = self.get_timedelta()
        next_bar = last_bar_timestamp + delta

        if self.chart_type == ChartType.OneDay:
            weekday = next_bar.isoweekday()
            if weekday == 6:
                return next_bar + timedelta(days=2)

            if weekday == 7:
                return next_bar + timedelta(days=1)

        return next_bar

    def wait_till_next_bar(self, latest_bar: datetime) -> None:
        next_bar = self.get_next_expected_bar(latest_bar)
        curr_bar = datetime.now(tz=timezone.utc) - timedelta(minutes=0)

        delta = int(next_bar.timestamp()) - int(curr_bar.timestamp())
        return 0 if delta < 0 else delta

    def get_historical_timeframe(self, historical_periods: int) -> Tuple[datetime, datetime]:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        return (
            start_date,
            start_date - timedelta(days=historical_periods)
        )

    @staticmethod
    def pre_market_open() -> bool:
        pre_market_start_time = datetime.now().replace(
            hour=8,
            minute=00,
            second=00,
            tzinfo=timezone.utc
        ).timestamp()

        market_start_time = datetime.now().replace(
            hour=13,
            minute=30,
            second=00,
            tzinfo=timezone.utc
        ).timestamp()

        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if market_start_time >= right_now >= pre_market_start_time:
            return True
        else:
            return False

    @staticmethod
    def post_market_open():
        post_market_end_time = datetime.now().replace(
            hour=00,
            minute=00,
            second=00,
            tzinfo=timezone.utc
        ).timestamp()

        market_end_time = datetime.now().replace(
            hour=20,
            minute=00,
            second=00,
            tzinfo=timezone.utc
        ).timestamp()

        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if post_market_end_time >= right_now >= market_end_time:
            return True
        else:
            return False

    @staticmethod
    def regular_market_open():
        market_start_time = datetime.now().replace(
            hour=13,
            minute=30,
            second=00,
            tzinfo=timezone.utc
        ).timestamp()

        market_end_time = datetime.now().replace(
            hour=20,
            minute=00,
            second=00,
            tzinfo=timezone.utc
        ).timestamp()

        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if market_end_time >= right_now >= market_start_time:
            return True
        else:
            return False
