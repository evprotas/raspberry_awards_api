import re
import operator
from raspberry_awards.models import Nomination
from raspberry_awards.serializers import IntervalsResponseSerializer
from raspberry_awards.interval import Interval

class NominationService:

    @staticmethod
    def __get_sorted_win_intervals():
        winners = Nomination.objects.filter(winner=True)
        winning_producers = {}
        for w in winners:
            for p in re.split(',|and ', w.producers):
                p = p.strip()
                if len(p) > 0:
                    try:
                        winning_producers[p] += [w.year]
                    except KeyError:
                        winning_producers[p] = [w.year]
    
        for y in winning_producers.values(): y.sort()
    
        intervals = []
        for wp in winning_producers.items():
            for i in range(len(wp[1])-1):
                intervals.append(Interval(producer=wp[0], previousWin=wp[1][i], followingWin=wp[1][i+1]))
        intervals.sort(key=operator.attrgetter('interval'))
        return intervals

    @staticmethod
    def get_min_win_interval():
        sorted_wind_intervals = NominationService.__get_sorted_win_intervals()
        min_interval_value = sorted_wind_intervals[0].interval
        return filter(lambda interval: interval.interval == min_interval_value, sorted_wind_intervals)

    @staticmethod
    def get_max_win_interval():
        sorted_wind_intervals = NominationService.__get_sorted_win_intervals()
        max_interval_value = sorted_wind_intervals[-1].interval
        return filter(lambda interval: interval.interval == max_interval_value, sorted_wind_intervals)