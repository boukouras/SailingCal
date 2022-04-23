from datetime import datetime,date,time,timezone,timedelta
import pytz
from dateutil.tz import gettz

## Υπερφόρτωση μεθόδων για προβολή αντίστοιχων αντικειμένων
class date(date):
    def __repr__(self):
        return self.strftime('%a %d/%m')
    def __str__(self):
        return self.strftime('%a %d/%m')

class time(time):
    def __repr__(self):
        return self.strftime('%H:%M')
    def __str__(self):
        return self.strftime('%H:%M')

#-------------------------------------------#
def date_analyze(txt):
    hour = f'{txt[8:10]}:{txt[10:12]}:{txt[12:14]}'
    whole_date = txt[:8]
    day = int(whole_date[6:])
    month = int(whole_date[4:6])
    year = whole_date[:4]
    if year[-1] == '1':
        year=year[:3] + '2'
    year = int(year)

    return date(year, month, day), time(int(txt[8:10]),int(txt[10:12]),int(txt[12:14]))


def to_datetime(date,time):
      return datetime.combine(date,time,tzinfo=pytz.timezone("Europe/Athens"))


def format_timestamp(datetime_obj):
    return datetime_obj.strftime('%Y%m%dT%H%M%S')