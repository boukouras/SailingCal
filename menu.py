

def menu():
    districts = ['Θερμαϊκός', 'Νησιά Αιγαίου']
    while True:
        print('1.Θερμαϊκός')
        print('2.Νησιά Αιγαίου')
        try:
            choice = int(input("\nΠαρακαλώ εισάγετε την επιλογή σας:"))
            if choice in range(1,3):break
            else:print("Εισάγετε 1 η 2.")
        except ValueError:
            print("Σφάλμα.\n")


    return districts[choice - 1]
