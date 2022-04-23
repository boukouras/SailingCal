from icalendar import Calendar, Event
import uuid
from dates import *
from Regatta import *



cal = Calendar()
cal['version'] = 2.0
cal['prodid']= "//Project//ical//Sailing_Calendar//EN"

#utc_offset = lambda offset: timezone(timedelta(seconds=offset))
#timezone(timedelta(seconds=10800)))

cal.add('BEGIN','VTIMEZONE')
cal.add('TZID','Europe/Athens')
cal.add('BEGIN','STANDARD')
cal.add('TZOFFSETFROM',timedelta(hours=0,minutes= 0,seconds=0))
cal.add('TZOFFSETTO',-timedelta(hours=3))
cal.add('TZNAME','UTC')
cal.add('END','STANDARD')
cal.add('END','VTIMEZONE')

def create_new_event(regatta):
    cal['name'] = regatta.district

    if isinstance(regatta, RaceType1):
        event = Event()
        current_time = datetime.now()
        event.add('transp', 'TRANSPARENT')
        event.add('summary', regatta.name)
        event['description'] = [{'Όμιλος':regatta.club_name, 'Διαδρομή':regatta.course, 'Απόσταση':regatta.length, 'Περιφέρεια':regatta.district}]
        uid = str(uuid.uuid4())
        event.add('uid', uid)
        uid = str(uuid.uuid4())
        event['dtstart'] = format_timestamp(to_datetime(regatta.stdate, regatta.sttime))
        event['created'] = format_timestamp(current_time)
        event['last-modified'] = format_timestamp(current_time)
        event['dtstamp'] = format_timestamp(current_time)
    if isinstance(regatta,RaceType2):
        event = Event()
        current_time = datetime.now()
        event.add('transp', 'TRANSPARENT')
        event.add('summary', regatta.name)
        event['description'] = [{'Όμιλος':regatta.club_name, 'Διαδορμή':regatta.course, 'Απόσταση':regatta.length, 'Περιφέρεια':regatta.district}]
        uid = str(uuid.uuid4())
        event.add('uid', uid)
        event['dtstart'] = format_timestamp(to_datetime(regatta.stdate, regatta.sttime))
        event['dtend'] = format_timestamp(to_datetime(regatta.todate, regatta.sttime))
        event['created'] =format_timestamp(current_time)
        event['last-modified'] =format_timestamp(current_time)
        event['dtstamp'] =format_timestamp(current_time)
    if isinstance(regatta,RaceType3):
        for reg in regatta.races:
            event = Event()
            current_time = datetime.now()
            event.add('transp', 'TRANSPARENT')
            event.add('summary', regatta.name)
            event['description'] = [{'Όμιλος':regatta.club_name,'Διαδρομή': reg.course,'Απόσταση':reg.length,'Περιφέρεια': regatta.district}]
            uid = str(uuid.uuid4())
            event.add('uid', uid)
            event['dtstart'] = format_timestamp(to_datetime(reg.stdate, reg.sttime))
            event['created'] = format_timestamp(current_time)
            event['last-modified'] =format_timestamp(current_time)
            event['dtstamp'] = format_timestamp(current_time)
        return event
    return event

def write_event(event, filename):
    cal.add_component(event)
    with open(filename, 'wb') as o:
        o.write(cal.to_ical())

