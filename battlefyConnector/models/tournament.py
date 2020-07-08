import dateutil.parser
import datetime


class Tournament:
    def __init__(self, startTime: datetime = dateutil.parser.isoparse("1970-01-01T00:00:00.000Z")):
        self.startTime = startTime
