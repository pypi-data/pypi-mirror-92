import time


class Timings(dict):
    """
    Context manager dictionary to record approximate execution times
    of code ran in the with block of this context manager. In each with
    block a key to accumulate the times can be specified. This is useful
    to measure the execution times of different parts of code running in a
    loop.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __call__(self, key):
        self.key = key
        if key not in self:
            self[key] = 0
        return self

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self[self.key] += (time.time() - self.start_time)

    @staticmethod
    def _get_string(values, keys, unit_str=None, decimal_places=3):
        s = ''
        for key in keys:
            s += key + ': {:0.' + str(decimal_places) + 'f}'
            if unit_str is not None:
                s += ' ' + unit_str
            s += ' | '
        return s[:-3].format(*values)

    def percentages(self, ret=False, decimal_places=3):
        summed = sum(self.values())
        percentages = [x / summed for x in self.values()]
        s = self._get_string(percentages, self.keys(), '%', decimal_places)
        if not ret:
            print(s)
        else:
            return s

    def seconds(self, ret=False, decimal_places=3):
        total = sum(self.values())
        s = self._get_string(list(self.values()) + [total], list(self.keys()) + ['total'], 'sec', decimal_places)
        if not ret:
            print(s)
        else:
            return s

    def summary(self):
        self.percentages()
        self.seconds()
