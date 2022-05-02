from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk

images = []

class Window(Tk):
    def __init__(self):
        super().__init__()
        self.title("Αγωνιστικό Ημερολόγιο Ανοιχτής Θαλάσσης")
        self.iconbitmap("images/Untitled-1.ico")
        self.geometry("1300x650")
        self.screen1 = Frame(self)
        self.screen2 = Frame(self)
        self.district =""


    def screen_1(self):
        self.screen1.pack()
        # frame = Frame(self,bd = 10) #bd = 15,relief = RAISED
        # frame.pack()
        img = Image.open("images/pexels-anthony-133606.jpg")
        photo = ImageTk.PhotoImage(img)
        images.append(photo)
        photo_label = Label(self.screen1, image=photo)
        photo_label.pack()
        enter_button = Button(self.screen1,text = "Είσοδος",command = self.screen_2, font="Times 12 italic bold" )
        enter_button.config(font=("Courier", 12))
        enter_button.pack(side = BOTTOM,anchor="s")

    def screen_2(self):
        choice = StringVar()
        def my_choice(clicked):
            nonlocal choice
            choice = clicked
            print(f"Choice get in my_choice func: {choice.get()}")
        def exit_from_program():
            msg = messagebox.askyesno("Έξοδος","Είστε σίγουροι ότι θέλετε να τερματίσετε το πρόγραμμα;")
            if msg == 1:
                exit()
            else:
                return

        districts = ['Ευβοϊκός', 'Κρήτη', 'Θερμαϊκός', 'Νησιά Αιγαίου', 'Θρακικό Πέλαγος', 'Νότια Πελοπόννησος',
                     'Ιόνιο', 'Πατραϊκός - Κορινθιακός', 'Κεντρική Ελλάδα', 'Σαρωνικός']
        self.screen1.pack_forget()
        self.screen2.grid(row = 0,column = 0,sticky = "NWES")
        left_frame = Frame(self.screen2)
        left_frame.grid(row = 0,column = 0,rowspan = 4,columnspan = 3)

        message = Label(left_frame,text="Παρακαλώ επιλέξτε την περιφέρεια που επιθυμείτε.")
        message.config(font=("Courier", 12))
        message.grid(row = 0,column = 0,columnspan = 3)

        clicked = StringVar()
        clicked.set(districts[0])  # default value
        drop = OptionMenu(left_frame, clicked, *districts)
        drop.grid(row = 2, column = 1)

        ok_button = Button(left_frame,text = "OK",command = lambda:my_choice(clicked))
        ok_button.grid(row = 6,column = 0)
        print(f"okButton{ok_button['command']}")

        exit_button = Button(left_frame,text = "Εξοδος",command = exit_from_program)
        exit_button.grid(row =6,column=3)


        self.district = choice.get()
        print(f"self.district: {self.district}")
        return self.district

    def races_preview(self,races):

        right_frame = Frame(self.screen2,bd = 15,padx=5,pady=5)
        right_frame.grid(row = 0,column=4,columnspan = 6,rowspan = 4)

        # Create label
        l = Label(right_frame, text=f"Αγωνιστικό Ημερολόγιο Περιφέρειας {self.district} ")
        l.config(font=("Courier", 14))
        l.grid(row = 0 ,column = 0,columnspan = 2)

        # Create text widget and specify size.
        T = Text(right_frame)

        T.grid(row = 3,column = 1)
        T.insert(INSERT,races)



