# SailingCal

from bs4 import BeautifulSoup
import requests
import csv


#Κλάση SailingCal
class SailingCal():
    #Συνάρτηση αρχικοποίησης
    def __init__(self, x,):
        self.x = x
        self.url = "https://www.offshore.org.gr/index.php?mx=Race_Schedule_2022&x=Program.xsl"
        self.xml = requests.get(self.url)
        self.soup = BeautifulSoup(self.xml.content, 'lxml')
        self.xml_tag = self.soup.findAll('district', attrs={'index':self.x})
        self.disctrict = str(self.xml_tag)
        self.disctricts = BeautifulSoup(self.disctrict, 'lxml')
        self.regattes = self.disctricts.findAll('regatta')

    #Συνάρτηση scrape όπου λαμβάνουμε τα δεδομένα
    def scrap(self):
        #url είναι η μεταβλητή της διεύθυνσης των δεδομένων που θέλουμε
        #Στην xml ζητάμε τα δεδομένα από την σελίδα αυτή, που είναι σε μορφή xml/xsl τα διαμορφώνουμε στην soup
        #xml_tag κρατάμε μόνο τα districts του index που θα επιλέξει ο χρήστης
        #regattes κρατάμε τα regatta του disctrict
        #f δημιουργούμε ένα csv αρχείο κάθε φορά ένα νέα, ή αν υπάρχει απλά διαγράφει τα προϋγούμενα δεδομένα και βάζει άλλα
        f = open('cal.csv', 'w', newline='')
        writer = csv.writer(f)

        for i in range(len(self.regattes)):
            if(i == 0):
                if(self.x == 0):
                    agwnes = "Σαρωνικός", ""
                elif(self.x == 3):
                    agwnes = "Κεντρική Ελλάδα", ""
                writer.writerow(agwnes)    
                agwnes = "Ώρα", "Ημέρα", "Όνομα", "Αγώνας", "Απόσταση", "Ομάδα"
                writer.writerow(agwnes)
            reggate = self.regattes[i]
            if(reggate.frdate.text == ""):
                race_tag = reggate.findAll('race')
                if(race_tag):
                    races_tags = reggate.findAll('race')
                    for j in range(len(races_tags)):
                        races = reggate.race
                        date = races_tags[j].stdate.text
                        hour = date[8:10] + ':' + date[10:12]
                        date = date[6:8] + '/' + date[4:6] + '/' + date[0:4]
                        length = races.length.text
                        clubname = reggate.clubname.text
                        course = races_tags[j]['name']
                        name = reggate["name"]
                        agwnes = hour, date, name, course, length, clubname
                        writer.writerow(agwnes)
                else:
                    races = reggate.race
                    date = races.stdate.text
                    hour = date[8:10] + ':' + date[10:12]
                    date = date[6:8] + '/' + date[4:6] + '/' + date[0:4]
                    length = races.length.text
                    clubname = reggate.clubname.text
                    course = races["name"]
                    name = reggate["name"]
                    agwnes = hour, date, name, course, length, clubname
                    writer.writerow(agwnes)
            elif(reggate.frdate.text != ""):
                if(reggate.todate.text == ""):
                    if(reggate.singlerace.text == "False"):
                        race_tag = reggate.findAll('race')
                        races_tags = reggate.findAll('race')
                        for j in range(len(races_tags)):
                            races = reggate.race
                            date = races_tags[j].stdate.text
                            hour = date[8:10] + ':' + date[10:12]
                            date = date[6:8] + '/' + date[4:6] + '/' + date[0:4]
                            length = races.length.text
                            clubname = reggate.clubname.text
                            course = races_tags[j]['name']
                            name = reggate["name"]
                            agwnes = hour, date, name, course, length, clubname
                            writer.writerow(agwnes)
                    else:
                        date = reggate.frdate.text
                        hour = str(date[8:10] + ':' + date[10:12])
                        date = str(date[6:8] + '/' + date[4:6] + '/' + date[0:4])
                        clubname = reggate.clubname.text
                        course = reggate.course.text
                        length = reggate.length.text
                        name = reggate["name"]
                        agwnes = hour, date, name, course, length, clubname
                        writer.writerow(agwnes)
                elif(reggate.todate.text != ""):
                    fdate = reggate.frdate.text
                    fhour = str(fdate[8:10] + ':' + fdate[10:12])
                    fdate = str(fdate[6:8] + '/' + fdate[4:6] + '/' + fdate[0:4])
                    tdate = reggate.todate.text
                    thour = str(tdate[8:10] + ':' + tdate[10:12])
                    tdate = str(tdate[6:8] + '/' + tdate[4:6] + '/' + tdate[0:4])
                    clubname = reggate.clubname.text
                    course = reggate.course.text
                    length = reggate.length.text
                    name = reggate["name"]
                    for i in range(2):
                        if(i == 0):
                            agwnes = thour, fdate, name, course, length, clubname, "Ημέρα έναρξη"
                        else:
                            agwnes = fhour, tdate, name, course, length, clubname, "Ημέρα λήξης"
                        writer.writerow(agwnes)

        f.close()

    #Συνάρτηση όπου ρωτάμε τον χρήστη για ποιά περιφέρεια ζητάει τα δεδομένα
    def inpt():
        post = False
        while(post == False):
            x =input("Παρακαλώ επιλέξτε από το 1 - 2 (1:Κεντρική Ελλάδα και 2:Σαρωνικός), <enter> για έξοδο.")
            if(x == '1' or x == '2'):
                if(x == '1'):
                    disname = 'Κεντρική Ελλάδα'
                    dis = 3
                elif(x == '2'):
                    disname = 'Σαρωνικός'
                    dis = 0
                post = True
                print('Η περιφέρεια που επιλέξατε είναι η ', disname)
            else:
                print('Παρακαλώ επιλέξτε ένα από τα δύο')
        return dis

    #Συνάρτηση main του προγράμματος
    def main():
        x = SailingCal.inpt()
        SailingCal.scrap(SailingCal(x))


if __name__ == '__main__':
    SailingCal.main()