import csv
import os.path
from lib.date import Date

DATA_FILENAME = "Data/data.csv"
FIELDNAMES = ["Index", "Date", "Type", "Amount", "Category"]

def init():
    with open(DATA_FILENAME, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

def menu():
    print("\n\t\t\t\t\tBudget\n")
    print("1. Add expense.")
    print("2. See entire transaction history.")
    print("3. See transaction history between two dates.")
    print("4. Exit.\n")

    return int(input("Input: "))

def getAddExpenseInput():
    transactionDate = Date(input("Enter the date of the transaction (MM-DD-YY): "))
    transactionType = input("Enter the type of the transaction (+/-): ")
    transactionAmount = int(input("Enter the amount of the transaction: "))
    transactionCategory = input("Enter the category of the transaction: ")

    return transactionDate, transactionType, transactionAmount, transactionCategory

def addExpense(transactionDate, transactionType, transactionAmount, transactionCategory):
    with open(DATA_FILENAME) as file:
        index = sum(1 for row in csv.reader(file))

    with open(DATA_FILENAME, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        writer.writerow({
            FIELDNAMES[0]: index,
            FIELDNAMES[1]: transactionDate,
            FIELDNAMES[2]: transactionType,
            FIELDNAMES[3]: transactionAmount,
            FIELDNAMES[4]: transactionCategory
        })

def display(startDate, endDate, displayAll=False):
    with open(DATA_FILENAME) as file:
        reader = csv.DictReader(file)
        rowsToPrint = []

        for row in reader:
            if Date(row[FIELDNAMES[1]]).compare(Date(startDate)) >= 0 and Date(row[FIELDNAMES[1]]).compare(Date(endDate)) <= 0:
                rowsToPrint.append(row)

        if len(rowsToPrint) == 0:
            if displayAll:
                print("No transactions logged yet.")
            else:
                print("No transactions found for this range.")
        else:
            print("\nIndex\t\tDate\t\t\tType\t\tAmount\t\tCategory")
            for row in rowsToPrint:
                print("{}\t\t{}\t\t{}\t\t${}\t\t{}".format(row[FIELDNAMES[0]], row[FIELDNAMES[1]], row[FIELDNAMES[2]], row[FIELDNAMES[3]], row[FIELDNAMES[4]]))

def getStartAndEndDates():
    startDate = input("Enter start date (MM-DD-YY): ")
    endDate = input("Enter end date (MM-DD-YY): ")

    return startDate, endDate


if __name__ == "__main__":

    # If the data file does not exist, create it
    if not os.path.isfile(DATA_FILENAME):
        print("Data file does not exist, creating now")
        init()

    # Main event loop
    inputChoice = -1
    while(inputChoice != 4):
        inputChoice = menu()
        
        if (inputChoice == 1):
            transactionDate, transactionType, transactionAmount, transactionCategory = getAddExpenseInput()
            addExpense(transactionDate, transactionType, transactionAmount, transactionCategory)
        elif (inputChoice == 2):
            display("00-00-00", "12-31-99", True)
        elif (inputChoice == 3):
            startDate, endDate = getStartAndEndDates()
            display(startDate, endDate) 
        elif (inputChoice == 4):
            print("Exiting")
            break
        else:
            print("Invalid input")