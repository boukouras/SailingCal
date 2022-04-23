from scrapping_code import *
from menu import menu
import requests
from calendar_ import *

#Αρχική ανάγνωση αρχείου από διαδίκτυο
URL = 'https://offshore.org.gr/index.php?mx=Race_Schedule_2022&x=Program.xsl'
response = requests.get(URL)

with open('file.xml', 'wb') as file:
    file.write(response.content)


#-------------------Άνοιγμα αρχείου ------------------#
try:
    file = open('file.xml', 'rb')
except FileNotFoundError:
    print("File Not Found")
    exit()


choice = menu()
wbs = Web_scrapper(file,choice)
races = wbs.retrieve_data()


filename = 'sailing_calendar.ics'

#------------Εκτύπωση Αγώνων Περιφέρειας ------------------#
for regatta in races:
    print(regatta)
    write_event(create_new_event(regatta),filename)

print(f"Ο αριθμός των αγώνων της περιφέρειας {races[0].district} είναι {len(races)}")


# with open("example.ics", 'wb') as f:
#     f.write(cal.to_ical())

