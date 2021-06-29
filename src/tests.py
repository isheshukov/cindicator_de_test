import unittest

from src.moving_average_logger import MovingAverageLogger


class TestMovingAverage(unittest.TestCase):
    def test_onevar_windowtoolarge(self):
        testlogger = MovingAverageLogger(fields=('o',), window_size=5, log_to_stdout=False, log_to_file=False)

        res = testlogger.process_payload({'k': {'o': 1, 's': 'test'}})

        self.assertEqual(None, res.o)

    def test_onevar_windowgood(self):
        testlogger = MovingAverageLogger(fields=('o',), window_size=3, log_to_stdout=False, log_to_file=False)

        testlogger.process_payload({'k': {'o': 1, 's': 'test'}})
        testlogger.process_payload({'k': {'o': 2, 's': 'test'}})

        res = testlogger.process_payload({'k': {'o': 3, 's': 'test'}})
        with self.subTest():
            self.assertEqual(6 / 3, res.o)

        res = testlogger.process_payload({'k': {'o': 2, 's': 'test'}})
        with self.subTest():
            self.assertEqual(7 / 3, res.o)

        res = testlogger.process_payload({'k': {'o': -3, 's': 'test'}})
        with self.subTest():
            self.assertEqual(2 / 3, res.o)

    def test_multiplevar_windowgood(self):
        testlogger = MovingAverageLogger(fields=('o', 'c', 'h'), window_size=3, log_to_stdout=False, log_to_file=False)

        testlogger.process_payload({'k': {'o': 1, 'c': 2, 'h': 3, 's': 'test'}})
        testlogger.process_payload({'k': {'o': 2, 'c': 3, 'h': 4, 's': 'test'}})
        res = testlogger.process_payload({'k': {'o': 3, 'c': 4, 'h': 5, 's': 'test'}})
        with self.subTest():
            self.assertEqual((6 / 3, 9 / 3, 12 / 3), (res.o, res.c, res.h))

        res = testlogger.process_payload({'k': {'o': 4, 'c': 5, 'h': 6, 's': 'test'}})
        with self.subTest():
            self.assertEqual((9 / 3, 12 / 3, 15 / 3), (res.o, res.c, res.h))


if __name__ == '__main__':
    unittest.main()
