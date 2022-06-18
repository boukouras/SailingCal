from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from scrape import SailingCalScraper
import os
from read_ical import readCal
import popup as pop

class GUI(Tk):
    def __init__(self):
        super().__init__() #Ορίζουμε την self ως root
        self.geometry('400x500') #Διάταξει παραθύρου
        self.resizable(False,False) #Απαγόρευση αλλαγής των διατάξεων του παραθύρου
        self.title('SailCal | Ημερολόγιο Ιστιοπλοΐας') #Τίτλος του παραθύρου
        self.iconbitmap(default='ico/sailing.ico') #Εικονίδιο παραθύρου


        #Λίστα με τις περιφέρειες σε σειρά όπως στο site
        self.districts = ['Σαρωνικός', 'Θερμαϊκός', 'Θρακικό Πέλαγος', 'Κεντρική Ελλάδα', 'Ευβοϊκός', 'Πατραϊκός - Κορινθιακός', 'Νότια Πελοπόννησος', 'Ιόνιο', 'Κρήτη', 'Νησιά Αιγαίου']

        #Σχεδιασμός παραθύρου
        Label(self, text='Καλώς ήλθατε στο SailCAL', font=25).pack()
        Label(self, text='(Τα δεδομένα πάρθηκαν από την Επιτροπή Ανοικτής Θαλάσσης)').pack(ipady=20)
        self.options = StringVar() #Ορίζουμε μεταβλητή για την επιλογή
        OptionMenu(self, self.options, *self.districts).pack(side=TOP, fill=X, expand=False, ipady=25)
        self.options.set('Παρακαλώ επιλέξτε περιφέρεια') #Αρχικοποιούμε την μεταβλητή επιλογή με την λέξη 'Περιφέρεια'

        Button(self, text='Λήψη Αρχείου', command=lambda: GUI.call(self)).pack(side = BOTTOM, fill = BOTH, expand=False, ipady= 25) #Button που καλεί την call για να κατεβάσει το αρχείο .ics ο χρήστης στο υπολοηιστή του



    def call(self):
        file = ''
        if self.options.get() == 'Παρακαλώ επιλέξτε περιφέρεια': # Έλεγχος για να δούμε αν ο χρήστης δεν έχει επιλέξει περιφέρεια
            pop.discterror() # Εμφάνιση νέου παραθύρου με το αντίστοιχο μήνυμα	
        else: # Βήματα αν ο χρήστης έχει επιλέξει περιφέρεια
            reqcomplete = False # Ορίζουμε λογική μεταβλητή ως False για μετέποιτα έλεγχο αν έχουν ολοκληρωθεί τα βήματα για να λάβει ο χρήστης το ημερολόγιο
            for i in range(len(self.districts)):
                if self.districts[i] == self.options.get():
                    self.number_of_district = i
            if reqcomplete == False: # Έλεγχος αν η λογική μεταβλητή είναι False
                file = filedialog.askdirectory() # Ζητάμε από τον χρήστη να ορίσει την θέσει που θα ήθελε να κατεβάσει το ημερολόγιο
                if os.path.exists(file+'/'+self.options.get()+'.ics'):
                    ask = pop.filedelreq()
                    if(ask == 'yes'):
                        scrape = SailingCalScraper(self.options.get(), self.number_of_district, file)#Καλούμε την κλάση scrape ορίζοντας την θέση του συνάρτησης στην λίστα
                        SailingCalScraper.scrape(scrape)
                        reqcomplete = True  # Ορίζουμε την λογική μεταβλητή True    
                    else:
                        reqcomplete = True
                else:
                    scrape = SailingCalScraper(self.options.get(), self.number_of_district, file)#Καλούμε την κλάση scrape ορίζοντας την θέση του συνάρτησης στην λίστα
                    SailingCalScraper.scrape(scrape)
                    reqcomplete = True  # Ορίζουμε την λογική μεταβλητή True
            if reqcomplete == True:
                send_to_mail = pop.sendmailreq()
                if send_to_mail == 'yes':
                    def request(provider): # Κλάση request για έλεγχο email
                        emailreqcomplete = False
                        if provider == 'google' or provider == 'microsoft':
                            pres = readCal(file+'/'+self.options.get()+'.ics', provider)
                            readCal.read_file(pres)
                    reqwin = Tk() # Ορίζουμε νέο παράθυρο
                    reqwin.resizable(False,False)
                    reqwin.title('Webmail πάροχος') # Ορίζουμε τον τίτλο του νέου παραθύρου
                    Label(reqwin, text='Παρακαλώ διαλέξτε τον δικό σας webmail πάροχο: ').pack() # Label 'Παρακαλώ εισάγετε το email σας'
 
                    Button(reqwin, text='Google', command= lambda:request('google')).pack(side=LEFT,fill=BOTH, expand=False, ipady=10, ipadx=25) # Button υποβολής που καλεί την κλάση request
                    Button(reqwin, text='Microsoft', command= lambda:request('microsoft')).pack(side=RIGHT,fill=BOTH, expand=False, ipady=10, ipadx=25) # Button υποβολής που καλεί την κλάση request

if __name__ == '__main__': # Έλεγχος αν το αρχείο είναι το main του προγράμματος
    app = GUI() # Ορίζουμε στην μεταβλητή app την κλάση GUI του παραθύρου
    app.mainloop() # mainloop της Tkinter