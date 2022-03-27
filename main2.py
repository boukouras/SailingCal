from scrapping_code import *
from menu import menu
#Αρχική ανάγνωση αρχείου από διαδίκτυο
# URL = 'https://offshore.org.gr/index.php?mx=Race_Schedule_2022&x=Program.xsl'
# response = requests.get(URL)
#
# with open('file.xml', 'wb') as file:
#     file.write(response.content)


#-------------------Άνοιγμα αρχείου ------------------#
try:
    file = open('file.xml', 'rb')
except FileNotFoundError:
    print("File Not Found")
    exit()


choice = menu()
wbs = Web_scrapper(file,choice)
races = wbs.retrieve_data()


for regatta in races:
    print(regatta)
print(f"Ο αριθμός των αγώνων της περιφέρειας {races[0].district} είναι {len(races)}")
# with open("example.ics", 'wb') as f:
#     f.write(cal.to_ical())