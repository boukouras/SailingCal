from icalendar import Calendar, Event
from apis import Google, Microsoft

class readCal: # Κλάση readCal, δημιουργήθηκε για να διαβάζει και να στέλνει τις πληροφορίες που θέλουμε στα αντίστοιχα APIs
    def __init__(self, filename, provider):
        self.filename = filename # Η θέση του αρχείου
        self.provider = provider # Πάροχος webmail
    
    def read_file(self):
        file = open(self.filename,'rb')
        filecal = Calendar.from_ical(file.read())
        for component in filecal.walk():
            eventdetails = {}
            if component.name == "VEVENT":
                eventdetails['summary'] = str(component.get('summary'))
                eventdetails['dtstart'] = str(component.decoded('dtstart')).replace(' ', 'T')
                eventdetails['dtend'] = str(component.decoded('dtend')).replace(' ', 'T')
                eventdetails['organizer'] = str(component.get('organizer'))
                eventdetails['location'] = str(component.get('location'))
                eventdetails['description'] = str(component.get('description'))

                if self.provider == 'google':
                    pres = Google(eventdetails)
                    Google.event(pres)
                elif self.provider == 'microsoft':
                    pres = Microsoft(eventdetails)
                    Microsoft.event(pres)
                    

        file.close()