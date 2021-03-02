class Date:
    def __init__(self, date):
        self.month = int(date.split('-')[0])
        self.day = int(date.split('-')[1])
        self.year = int(date.split('-')[2])

    def __str__(self):
        return "{}-{}-{}".format(self.month, self.day, self.year)

    def compare(self, other):
        if other.year > self.year:
            return -1
        elif other.year < self.year:
            return 1
        elif other.month > self.month:
            return -1
        elif other.month < self.month:
            return 1
        elif other.day > self.day:
            return -1
        elif other.day < self.day:
            return 1
        else:
            return 0