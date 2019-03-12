import time
import unittest

import WordClock


class WorldClockTestMethod(unittest.TestCase):

    def test1322(self):
        tt = time.strptime("13:22", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertEqual(clock._currentHour, 1)
        self.assertEqual(clock._currentMinute, 22)
        self.assertIn("ONE", clock.get_words())
        self.assertIn("PM", clock.get_words())
        self.assertIn("TWENTY", clock.get_words())
        self.assertIn("JUST", clock.get_words())
        self.assertIn("AFTER", clock.get_words())

    def test2145(self):
        tt = time.strptime("21:45", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertIn("TEN", clock.get_words())
        self.assertIn("PM", clock.get_words())
        self.assertIn("A", clock.get_words())
        self.assertIn("QUARTER", clock.get_words())
        self.assertIn("TO", clock.get_words())

    def test2358(self):
        tt = time.strptime("23:58", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertIn("TWELVE", clock.get_words())
        self.assertIn("AM", clock.get_words())
        self.assertIn("JUST", clock.get_words())
        self.assertIn("BEFORE", clock.get_words())

    def test0003(self):
        tt = time.strptime("00:03", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertIn("TWELVE", clock.get_words())
        self.assertIn("AM", clock.get_words())
        self.assertIn("JUST", clock.get_words())
        self.assertIn("FIVE", clock.get_words())

    def test1158(self):
        tt = time.strptime("11:58", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertIn("TWELVE", clock.get_words())
        self.assertIn("PM", clock.get_words())
        self.assertIn("JUST", clock.get_words())
        self.assertIn("BEFORE", clock.get_words())

    def test1145(self):
        tt = time.strptime("11:45", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertIn("TWELVE", clock.get_words())
        self.assertIn("PM", clock.get_words())
        self.assertIn("QUARTER", clock.get_words())
        self.assertIn("A", clock.get_words())
        self.assertIn("TO", clock.get_words())

    def test1202(self):
        tt = time.strptime("12:02", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertIn("TWELVE", clock.get_words())
        self.assertIn("PM", clock.get_words())
        self.assertIn("JUST", clock.get_words())
        self.assertIn("AFTER", clock.get_words())

    def test0230(self):
        tt = time.strptime("02:30", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertIn("TWO", clock.get_words())
        self.assertIn("AM", clock.get_words())
        self.assertIn("HALF", clock.get_words())
        self.assertIn("PAST", clock.get_words())

    def test1058(self):
        tt = time.strptime("10:58", "%H:%M")
        clock = WorldClock.WorldClock(tt)
        self.assertIn("ELEVEN", clock.get_words())
        self.assertIn("AM", clock.get_words())
        self.assertIn("BEFORE", clock.get_words())
        self.assertIn("JUST", clock.get_words())


if __name__ == '__main__':
    unittest.main()
