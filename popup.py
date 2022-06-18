import pandas as pd
from tkinter import Tk, messagebox

def verifyrcode(code):
    result = messagebox.showinfo(title=verifyrcode.__name__, message='Ο Κωδικός επαλήθευσης σας είναι: '+code+'\Έχει γίνει ήδη αντιγραφή, μπορείτε να τον κάνετε επικόλληση')
    df=pd.DataFrame([str(code)])
    df.to_clipboard(index=False,header=False)

def sendemailreq():
    result = messagebox.askquestion(title=sendemailreq.__name__, message="\nΘα θέλατε να σας αποστείλουμε το iCalendar αρχείο στο email σας;")
    return result

def filedelreq():
    result = messagebox.askquestion(title=filedelreq.__name__, message="Το αρχείο που θέλετε να δημιουργήσεται υπάρχει ήδη, αν συνεχίσουμε στο προϋγούμενο αρχείο θα αλλαχθούν στα δεδομένα του!\nΘέλετε να προχωρήσουμε;")
    return result

def sendmailreq():
    result = messagebox.askquestion(title=sendmailreq.__name__, message="\nΘα θέλατε να σας αποστείλουμε το iCalendar αρχείο στο email σας;")
    return result
def discterror():
    messagebox.showerror(title = discterror.__name__, message='Πρόβλημα με την επιλογή σας!\nΔεν έχετε επιλέξει περιφέρεια, παρακαλώ επιλέξτε μία!')