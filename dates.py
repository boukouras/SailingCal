from datetime import datetime,date,time

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
    year = int(whole_date[:4])
    return date(year, month, day).isoformat(), time(int(txt[8:10]),int(txt[10:12]),int(txt[12:14]))#datetime.strptime(hour, '%H:%M:%S').time()   #.fromisoformat(hour)

def date_to_isoformat(date,time):
    string = ""
    string += date[:4] + date[5:7] + date[8:10] + 'T' + str(time.strftime("%H")) + str(time.strftime("%M")) + str(time.strftime("%S"))
    return string

