import csv
import logging
from collections import defaultdict, namedtuple, deque
from datetime import datetime
from pathlib import Path
from statistics import mean

logger = logging.getLogger(__name__)

class MovingAverageLogger:
    def __init__(self, fields=('o', 'c', 'h', 'l', 'v', 'n', 'q', 'V', 'Q'), window_size=5, log_to_stdout=True, log_to_file=True):
        """
        Moving Average Logger class. Calculates simple moving average and logs to .csv file and/or stdout.

        :param fields: Fields to log. Default is ('o', 'c', 'h', 'l', 'v', 'n', 'q', 'V', 'Q').
        :param log_to_file: Enable logging to .csv file. Defaults to true.
        :param log_to_stdout: Enable logging to stdout. Defaults to true.
        """

        # Dict holding averages
        # {'btcbnb': {'buffer': deque(), 'avg': PayloadData(o=0, c=0, h=0, l=0, v=0, n=0, q=0, V=0, Q=0)}}
        self.log_to_stdout = log_to_stdout
        self.log_to_file = log_to_file

        self.startup_date = datetime.now()

        self.fields = fields
        self.window_size = window_size
        self.PayloadData = namedtuple('PayloadData', self.fields, defaults=(None,) * len(self.fields))

        self.symbol_avgs = defaultdict(lambda: dict(buffer=deque(maxlen=window_size),
                                                    avg=self.PayloadData()))

    def __log(self, symbol, data):
        """
        Log function

        :param symbol: Currency pair to log
        :param data: Data
        :return:
        """
        current_time = datetime.now()

        if self.log_to_stdout:
            logger.info(f"{symbol},{data}")

        if self.log_to_file:
            Path("./logs").mkdir(parents=True, exist_ok=True)
            with open(f'./logs/{symbol}-{self.startup_date}.csv', 'a', newline='') as log:
                fields = ('time',) + self.fields
                writer = csv.DictWriter(log, fieldnames=fields)

                if log.tell() == 0:
                    writer.writeheader()

                row = data._asdict()
                row.update({'time': current_time})

                writer.writerow(row)

    def process_payload(self, payload) -> 'self.PayloadData':
        """
        Process payload using cumulative sum average

        :param payload: Dictionary in Binance candle response format
        :return: Latest rolling average
        """

        if 'k' in payload:
            pk = payload['k']
        else:
            return

        symbol = pk['s']
        pdata = self.PayloadData(**{f: float(pk[f]) for f in self.fields})

        # Add data to buffer
        self.symbol_avgs[symbol]['buffer'].append(pdata)

        # Wait until the buffer is full
        if len(self.symbol_avgs[symbol]['buffer']) < self.window_size:
            return self.symbol_avgs[symbol]['avg']

        # When the buffer is full compute SMA
        new_sma = self.PayloadData(*map(mean, zip(*self.symbol_avgs[symbol]['buffer'])))

        self.symbol_avgs[symbol]['avg'] = new_sma

        self.__log(symbol, new_sma)

        return new_sma
