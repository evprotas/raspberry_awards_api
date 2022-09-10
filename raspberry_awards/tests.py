from django.test import TestCase
from django.test import Client
from raspberry_awards.models import Nomination
from raspberry_awards.serializers import IntervalSerializer

class LosersDontCountTestCase(TestCase):
    c = Client()

    def setUp(self):

        self.c = Client()

        Nomination.objects.create(title="Loser 1990",
                                  year=1990,
                                  producers="Loser producer 1",
                                  studios="Loser studio",
                                  winner=False)

        Nomination.objects.create(title="Loser 1991",
                                  year=1991,
                                  producers="Loser producer 1",
                                  studios="Loser studio",
                                  winner=False)

        Nomination.objects.create(title="Winner 1990",
                                  year=1990,
                                  producers="Winner producer 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1992",
                                  year=1992,
                                  producers="Winner producer 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Loser 1980",
                                  year=1980,
                                  producers="Loser producer 2",
                                  studios="Loser studio",
                                  winner=False)

        Nomination.objects.create(title="Loser 1999",
                                  year=1999,
                                  producers="Loser producer 2",
                                  studios="Loser studio",
                                  winner=False)

        Nomination.objects.create(title="Winner 1994",
                                  year=1994,
                                  producers="Winner producer 2",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1998",
                                  year=1998,
                                  producers="Winner producer 2",
                                  studios="Winner studio",
                                  winner=True)


    def test_losers_dont_count_min(self):
        response = self.c.get('/awards/intervals')
        min_intervals = IntervalSerializer(data=response.json().get('min'), many=True)
        self.assertTrue(min_intervals.is_valid())
        for i in min_intervals.create(min_intervals.validated_data):
            self.assertEqual(i.interval, 2)
            self.assertEqual(i.producer, "Winner producer 1")

    def test_losers_dont_count_max(self):
        response = self.c.get('/awards/intervals')
        max_intervals = IntervalSerializer(data=response.json().get('max'), many=True)
        self.assertTrue(max_intervals.is_valid())
        for i in max_intervals.create(max_intervals.validated_data):
            self.assertEqual(i.interval, 4)
            self.assertEqual(i.producer, "Winner producer 2")

class MustWinTwiceTestCase(TestCase):
    c = Client()

    def setUp(self):

        self.c = Client()

        Nomination.objects.create(title="Loser 1990",
                                  year=1990,
                                  producers="Loser producer 1",
                                  studios="Loser studio",
                                  winner=False)

        Nomination.objects.create(title="Loser 1991",
                                  year=1991,
                                  producers="Loser producer 1",
                                  studios="Loser studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1990",
                                  year=1990,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1993",
                                  year=1993,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Loser 1980",
                                  year=1980,
                                  producers="Loser producer 2",
                                  studios="Loser studio",
                                  winner=False)

        Nomination.objects.create(title="Loser 1999",
                                  year=1999,
                                  producers="Loser producer 2",
                                  studios="Loser studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1994",
                                  year=1994,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1999",
                                  year=1999,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)


    def test_must_win_twice_min(self):
        response = self.c.get('/awards/intervals')
        min_intervals = IntervalSerializer(data=response.json().get('min'), many=True)
        self.assertTrue(min_intervals.is_valid())
        for i in min_intervals.create(min_intervals.validated_data):
            self.assertEqual(i.interval, 3)
            self.assertEqual(i.producer, "Winner 3")

    def test_must_win_twice_max(self):
        response = self.c.get('/awards/intervals')
        max_intervals = IntervalSerializer(data=response.json().get('max'), many=True)
        self.assertTrue(max_intervals.is_valid())
        for i in max_intervals.create(max_intervals.validated_data):
            self.assertEqual(i.interval, 5)
            self.assertEqual(i.producer, "Winner 4")

class SeparatorTestCase(TestCase):
    c = Client()

    def setUp(self):

        self.c = Client()

        Nomination.objects.create(title="Winner 1990",
                                  year=1990,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1993",
                                  year=1993,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1989",
                                  year=1989,
                                  producers="Winner 2, Producer123",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1991",
                                  year=1991,
                                  producers="Producer432 and Winner 2",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1980",
                                  year=1980,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1985",
                                  year=1985,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1994",
                                  year=1994,
                                  producers="Producer 777, Produce 666 and Winner 4",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2007",
                                  year=2007,
                                  producers="Producer111, Winner 4, Producer 2423 and Producer 555",
                                  studios="Winner studio",
                                  winner=True)


    def test_separator_min(self):
        response = self.c.get('/awards/intervals')
        min_intervals = IntervalSerializer(data=response.json().get('min'), many=True)
        self.assertTrue(min_intervals.is_valid())
        for i in min_intervals.create(min_intervals.validated_data):
            self.assertEqual(i.interval, 2)
            self.assertEqual(i.producer, "Winner 2")

    def test_separator_max(self):
        response = self.c.get('/awards/intervals')
        max_intervals = IntervalSerializer(data=response.json().get('max'), many=True)
        self.assertTrue(max_intervals.is_valid())
        for i in max_intervals.create(max_intervals.validated_data):
            self.assertEqual(i.interval, 13)
            self.assertEqual(i.producer, "Winner 4")

class MultipleProducersPerMovieTestCase(TestCase):
    c = Client()

    def setUp(self):

        self.c = Client()

        Nomination.objects.create(title="Winner 1990",
                                  year=1990,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1993",
                                  year=1993,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1989",
                                  year=1989,
                                  producers="Winner 2, Producer123 and Winner 5",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1990",
                                  year=1990,
                                  producers="Winner 5 and Winner 2",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1980",
                                  year=1980,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1985",
                                  year=1985,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1992",
                                  year=1992,
                                  producers="Winner 6, Winner 7, Producer 9994 and Winner 4",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2007",
                                  year=2007,
                                  producers="Winner 7, Winner 4, Producer 2423, Producer 555 and Winner 6",
                                  studios="Winner studio",
                                  winner=True)


    def test_multiple_producers_per_movie_min(self):
        response = self.c.get('/awards/intervals')
        min_intervals = IntervalSerializer(data=response.json().get('min'), many=True)
        self.assertTrue(min_intervals.is_valid())
        min_results = min_intervals.create(min_intervals.validated_data)
        self.assertEqual(len(min_results), 2)
        self.assertIn("Winner 2", map(lambda x : x.producer, min_results))
        self.assertIn("Winner 5", map(lambda x : x.producer, min_results))

        for i in min_results:
            self.assertEqual(i.interval, 1)
            self.assertIn(i.producer, ["Winner 2", "Winner 5"])

    def test_multiple_producers_per_movie_max(self):
        response = self.c.get('/awards/intervals')
        max_intervals = IntervalSerializer(data=response.json().get('max'), many=True)
        self.assertTrue(max_intervals.is_valid())
        max_results = max_intervals.create(max_intervals.validated_data)
        self.assertEqual(len(max_results), 3)
        self.assertIn("Winner 7", map(lambda x : x.producer, max_results))
        self.assertIn("Winner 6", map(lambda x : x.producer, max_results))
        self.assertIn("Winner 4", map(lambda x : x.producer, max_results))
        for i in max_intervals.create(max_intervals.validated_data):
            self.assertEqual(i.interval, 15)
            self.assertIn(i.producer, ["Winner 4", "Winner 6", "Winner 7"])

class MultipleProducersSameIntervalTestCase(TestCase):
    c = Client()

    def setUp(self):

        self.c = Client()

        Nomination.objects.create(title="Winner 1990",
                                  year=1990,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1992",
                                  year=1992,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1989",
                                  year=1989,
                                  producers="Winner 2",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1991",
                                  year=1991,
                                  producers="Winner 2",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1993",
                                  year=1993,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1995",
                                  year=1995,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1994",
                                  year=1994,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1997",
                                  year=1997,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1983",
                                  year=1983,
                                  producers="Winner 5",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1988",
                                  year=1988,
                                  producers="Winner 5",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1982",
                                  year=1982,
                                  producers="Winner 6",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1987",
                                  year=1987,
                                  producers="Winner 6",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2000",
                                  year=2000,
                                  producers="Winner 7",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2005",
                                  year=2005,
                                  producers="Winner 7",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2010",
                                  year=2010,
                                  producers="Winner 8",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2015",
                                  year=2015,
                                  producers="Winner 8",
                                  studios="Winner studio",
                                  winner=True)

    def test_multiple_producers_same_interval_min(self):
        response = self.c.get('/awards/intervals')
        min_intervals = IntervalSerializer(data=response.json().get('min'), many=True)
        self.assertTrue(min_intervals.is_valid())
        min_results = min_intervals.create(min_intervals.validated_data)
        self.assertEqual(len(min_results), 3)
        self.assertIn("Winner 1", map(lambda x : x.producer, min_results))
        self.assertIn("Winner 2", map(lambda x : x.producer, min_results))
        self.assertIn("Winner 3", map(lambda x : x.producer, min_results))

        for i in min_results:
            self.assertEqual(i.interval, 2)
            self.assertIn(i.producer, ["Winner 1", "Winner 2", "Winner 3"])

    def test_multiple_producers_same_interval_max(self):
        response = self.c.get('/awards/intervals')
        max_intervals = IntervalSerializer(data=response.json().get('max'), many=True)
        self.assertTrue(max_intervals.is_valid())
        max_results = max_intervals.create(max_intervals.validated_data)
        self.assertEqual(len(max_results), 4)
        self.assertIn("Winner 7", map(lambda x : x.producer, max_results))
        self.assertIn("Winner 6", map(lambda x : x.producer, max_results))
        self.assertIn("Winner 5", map(lambda x : x.producer, max_results))
        self.assertIn("Winner 8", map(lambda x : x.producer, max_results))
        for i in max_intervals.create(max_intervals.validated_data):
            self.assertEqual(i.interval, 5)
            self.assertIn(i.producer, ["Winner 5", "Winner 6", "Winner 7", "Winner 8"])

class MoreThanTwoWinsTestCase(TestCase):
    c = Client()

    def setUp(self):

        self.c = Client()

        Nomination.objects.create(title="Winner 1990",
                                  year=1990,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1992",
                                  year=1992,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1993",
                                  year=1993,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1994",
                                  year=1994,
                                  producers="Winner 2",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1996",
                                  year=1996,
                                  producers="Winner 2",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1980",
                                  year=1980,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1985",
                                  year=1985,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2000",
                                  year=2000,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2007",
                                  year=2007,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2010",
                                  year=2010,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)

    def test_more_than_two_wins_min(self):
        response = self.c.get('/awards/intervals')
        min_intervals = IntervalSerializer(data=response.json().get('min'), many=True)
        self.assertTrue(min_intervals.is_valid())
        min_results = min_intervals.create(min_intervals.validated_data)
        self.assertEqual(len(min_results), 1)
        
        for i in min_results:
            self.assertEqual(i.interval, 1)
            self.assertEqual(i.producer, "Winner 1")

    def test_more_than_two_wins_max(self):
        response = self.c.get('/awards/intervals')
        max_intervals = IntervalSerializer(data=response.json().get('max'), many=True)
        self.assertTrue(max_intervals.is_valid())
        max_results = max_intervals.create(max_intervals.validated_data)
        self.assertEqual(len(max_results), 1)
        for i in max_intervals.create(max_intervals.validated_data):
            self.assertEqual(i.interval, 7)
            self.assertEqual(i.producer, "Winner 4")

class NonConsecutiveWinsTestCase(TestCase):
    c = Client()

    def setUp(self):

        self.c = Client()

        Nomination.objects.create(title="Winner 1990",
                                  year=1990,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1992",
                                  year=1992,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1994",
                                  year=1994,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1996",
                                  year=1996,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1998",
                                  year=1998,
                                  producers="Winner 1",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1980",
                                  year=1980,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 1981",
                                  year=1981,
                                  producers="Winner 3",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2000",
                                  year=2000,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)

        Nomination.objects.create(title="Winner 2003",
                                  year=2003,
                                  producers="Winner 4",
                                  studios="Winner studio",
                                  winner=True)

    def test_non_consecutive_wins_dont_count_max(self):
        response = self.c.get('/awards/intervals')
        max_intervals = IntervalSerializer(data=response.json().get('max'), many=True)
        self.assertTrue(max_intervals.is_valid())
        max_results = max_intervals.create(max_intervals.validated_data)
        self.assertEqual(len(max_results), 1)
        for i in max_intervals.create(max_intervals.validated_data):
            self.assertEqual(i.interval, 3)
            self.assertEqual(i.producer, "Winner 4")
