import csv
import os.path

DATA_FILENAME = "Data/data.csv"
FIELDNAMES = ["Index", "Date", "Type", "Amount", "Category"]

def init():
    with open(DATA_FILENAME, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

def menu():
    print("\n\t\t\t\t\tBudget\n")
    print("1. Add expense.")
    print("2. See transaction history.")
    print("3. Exit.\n")

    return int(input("Input: "))

def createDict():
    print("")

def addExpense():
    with open(DATA_FILENAME, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)


if __name__ == "__main__":

    # Check if data file exists
    if (os.path.isfile(DATA_FILENAME)):
        fileFlag = True   
    else:
        fileFlag = False


    # If the data file does not exist, create it
    if not fileFlag:
        print("Data file does not exist, creating now")
        init()


    # Main event loop
    inputChoice = -1
    while(inputChoice != 3):
        inputChoice = menu()
        
        if (inputChoice == 1):
            # addExpense()
            print("Add")
        elif (inputChoice == 2):
            print("Under construction")
        elif (inputChoice == 3):
            print("Exiting")
            break
        else:
            print("Invalid input")