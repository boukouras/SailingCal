from scrapping_code import *
from menu import menu
import requests
from calendar_ import *
from graphic_interface import *





if __name__ == '__main__':
    # Αρχική ανάγνωση αρχείου από διαδίκτυο
    URL = 'https://offshore.org.gr/index.php?mx=Race_Schedule_2022&x=Program.xsl'
    response = requests.get(URL)

    with open('file.xml', 'wb') as file:
        file.write(response.content)

    # -------------------Άνοιγμα αρχείου ------------------#
    try:
        file = open('file.xml', 'rb')
    except FileNotFoundError:
        print("File Not Found")
        exit()


    window = Window()
    window.screen_1()

    choice = window.district
    print(choice)
    wbs = Web_scrapper(file,choice)
    races = wbs.retrieve_data()

    window.races_preview(races)







    filename = 'sailing_calendar.ics'

#------------Εκτύπωση Αγώνων Περιφέρειας ------------------#
    global txt
    txt = ""
    for regatta in races:
        print(regatta)
        txt += str(regatta)
    # print(txt)
    #     #write_event(create_new_event(regatta),filename)
    #
    # print(f"Ο αριθμός των αγώνων της περιφέρειας {races[0].district} είναι {len(races)}")




    window.mainloop()