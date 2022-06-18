from bs4 import BeautifulSoup
from datetime import datetime
import requests
from icalendar import Calendar, Event, vCalAddress, vText
import pytz

#Κλάση SailingCal
class SailingCalScraper: # Κλάση SailingCalScraper
    def __init__(self, name, number_of_disctrict, *args): # Αρχικοποιούμε τις μεταβλητές
        self.name = str(name)
        self.number_of_disctrict = number_of_disctrict # Αρχικοποιούμε την τιμή για την θέση της περιφέρειας, το νούμερο στον πίνακα
        if '@' in args[0]: # Ελέγχουμε αν ο χρήστης μας έδωσε που να αποθηκεύσουμε το αρχείο στον υπολογιστή του
            self.ical = False
            self.email = str(args[0])
            self.provider = str(args[1])
        else:
            self.place = str(args[0]) # Αρχικοποιούμε την θέση στην μεταβλητή place
            self.ical = True
        self.url = "https://www.offshore.org.gr/index.php?mx=Race_Schedule_2022&x=Program.xsl" # Αρχικοποιούμε στην μεταβλητή αυτή το link του ημερολογίου για web scrape
        self.xml = requests.get(self.url) # Θέτουμε στην μεταβλητή self.xml όλο τον 'κώδικα' του site
        self.soup = BeautifulSoup(self.xml.content, 'lxml') # BeautifulSoup τον κώδικα του site
        self.xml_tag = self.soup.findAll('district', attrs={'index':self.number_of_disctrict}) # Κρατάμε μόνο τον κώδικα της περιφέρειας με τον αριθμό που έχει δώσει ο χρήστης
        self.disctrict = str(self.xml_tag) # Μετατρέπουμε την xml_tag σε str Και την θέτουμε στην districs μεταβλητή
        self.disctricts = BeautifulSoup(self.disctrict, 'lxml') # BeautifulSoup την μεταβλητή district στην districts μέ τρόπο lxml
        self.regattes = self.disctricts.findAll('regatta') # Κρατάμε τις regattes της districts στην regattes

    def events(self, detail):
        event = Event()
        event.add('summary', vText(detail['summary']))
        event.add('dtstart', detail['dtstart'])
        event.add('dtend', detail['dtend'])
        event['organizer'] = detail['organizer']
        event['location'] = vText(detail['location'])
        event['description'] = vText(detail['description'])

        self.cal.add_component(event)

    def scrape(self): # Συνάρτηση scrape
        if self.ical == True:
            file = open(self.place+'/'+self.name+'.ics', 'wb')
            self.cal = Calendar()
        for i in range(len(self.regattes)): # Eπανάληψη για όσες regattes υπάρχουν
            reggate = self.regattes[i] # Θέτουμε την εκάστοτε reggate με βάση την επανάληψη στην μεταβλητή reggate 
            if(reggate.frdate.text == ""): # Έλεγχος για το αν δεν υπάρχει ημ/νία για να ελέξουμε πιο κάτω αντός της reggate για races tags
                race_tag = reggate.findAll('race') # Θέτουμε στην μεταβλητή race_tag όλες τις race εντώς της reggate
                if(race_tag): # Αν έχει βρεθεί race
                    races_tags = reggate.findAll('race')
                    for j in range(len(races_tags)): # Επανάληψη για όσα races βρέθηκαν
                        races = reggate.race # Ορίζουμε την μεταβλητή races με τα races της reggate
                        date = races_tags[j].stdate.text # Ορίζουμε την ημερομινεία και ώρα	
                        detail = {
                            'organizer': reggate.clubname.text,
                            'location':races_tags[j]['name'], 
                            'summary':reggate["name"], 
                            'syear':date[0:4], 
                            'description': 'Όμιλος: '+reggate.clubname.text+' - ' +'Διαδρομή: '+races_tags[j]['name']+' - '+'Απόσταση: '+races.length.text,
                            'dtstart':datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),tzinfo=pytz.utc),
                            'dtend':datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),tzinfo=pytz.utc)
                        }
                        SailingCalScraper.events(self, detail)
                else:
                    races = reggate.race # Ορίζουμε την μεταβλητή races με τα races της reggate
                    date = races.stdate.text # Ορίζουμε την ημερομινεία και ώρα	
                        
                    detail = {
                        'organizer': reggate.clubname.text,
                        'location':races_tags['name'], 
                        'summary':reggate["name"], 
                        'syear':date[0:4], 
                        'description': 'Όμιλος: '+reggate.clubname.text+' - ' +'Διαδρομή: '+races_tags['name']+' - '+'Απόσταση: '+races.length.text,
                        'dtstart':datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),tzinfo=pytz.utc),
                        'dtend':datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),tzinfo=pytz.utc)
                    }
                    SailingCalScraper.events(self, detail)

                
            elif(reggate.frdate.text != ""): # Έλεγχος αν υπάρχει ημερομινεία
                if(reggate.todate.text == ""): # Έλεγχος αν δεν υπάρχει ημερομινεία λήξης
                    if(reggate.singlerace.text == "False"): # Έλεγχος αν δεν είναι singlrace
                        race_tag = reggate.findAll('race') # Θέτουμε όλες τις races της reggata
                        races_tags = reggate.findAll('race') # Θέτουμε όλες τις races της reggata
                        for j in range(len(races_tags)): # Επαναλήψεις για όσα races υπάρχουν
                            races = reggate.race # Ορίζουμε την μεταβλητή races με τα races της reggate
                            date = races_tags[j].stdate.text # Ορίζουμε την ημερομινεία και ώρα	
                            detail = {
                                'organizer': reggate.clubname.text,
                                'location':races_tags[j]['name'], 
                                'summary':reggate["name"], 
                                'syear':date[0:4], 
                                'description': 'Όμιλος: '+reggate.clubname.text+' - ' +'Διαδρομή: '+races_tags[j]['name']+' - '+'Απόσταση: '+races.length.text,
                                'dtstart':datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),tzinfo=pytz.utc),
                                'dtend':datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),tzinfo=pytz.utc)
                            }
                            SailingCalScraper.events(self, detail)
    
                            
                    else: # Έλεγχος αν είναι singlrace
                        date = reggate.frdate.text # Ορίζουμε την ημερομινεία και ώρα	
                        detail = {
                            'organizer': reggate.clubname.text,
                            'location':reggate.course.text, 
                            'summary':reggate["name"], 
                            'syear':date[0:4], 
                            'description': 'Όμιλος: '+reggate.clubname.text+' - ' +'Διαδρομή: '+reggate.course.text+' - '+'Απόσταση: '+reggate.length.text,
                            'dtstart':datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),tzinfo=pytz.utc),
                            'dtend':datetime(int(date[0:4]),int(date[4:6]),int(date[6:8]),int(date[8:10]),int(date[10:12]),tzinfo=pytz.utc)
                        }
                        SailingCalScraper.events(self, detail)

                elif(reggate.todate.text != ""): # Έλεγχος αν υπάρχει ημερομινεία λήξης
                    fdate = reggate.frdate.text # Ορίζουμε την ημερομινεία έναρξης
                    tdate = reggate.todate.text
                    detail = {
                        'organizer': reggate.clubname.text,
                        'location':reggate.course.text, 
                        'summary':reggate["name"], 
                        'syear':date[0:4], 
                        'description': 'Όμιλος: '+reggate.clubname.text+' - ' +'Διαδρομή: '+reggate.course.text+' - '+'Απόσταση: '+reggate.length.text,
                        'dtstart':datetime(int(fdate[0:4]),int(fdate[4:6]),int(fdate[6:8]),int(fdate[8:10]),int(fdate[10:12]),tzinfo=pytz.utc),
                        'dtend':datetime(int(tdate[0:4]),int(tdate[4:6]),int(tdate[6:8]),int(tdate[8:10]),int(tdate[10:12]),tzinfo=pytz.utc)
                    }
                    SailingCalScraper.events(self, detail)
        
        file.write(self.cal.to_ical())
        file.close()
