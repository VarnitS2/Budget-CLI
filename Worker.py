import csv
import os
from pathlib import Path
from lib.date import Date

DATA_DIRECTORY = "data"
DATA_FILENAME = "data/data.csv"
FIELDNAMES = ["Index", "Date", "Type", "Amount", "Category"]

NOTES_FILENAME = "data/notes.txt"

def dataInit():
    Path(DATA_DIRECTORY).mkdir(parents=True, exist_ok=True)

    with open(DATA_FILENAME, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

def menu():
    print("\n")
    print("Budget".center(170))
    print("\n1. Add transaction.")
    print("2. See entire transaction history.")
    print("3. See transaction history between two dates.")
    print("4. Notes.")
    print("5. Exit.\n")

    return int(input("-> "))

def getAddTransactionInput():
    transactionDate = Date(input("Enter the date of the transaction (MM/DD/YY): "))
    transactionType = input("Enter the type of the transaction (+/-): ")
    transactionAmount = float(input("Enter the amount of the transaction: "))
    transactionCategory = input("Enter the category of the transaction: ")

    return transactionDate, transactionType, transactionAmount, transactionCategory

def addTransaction(transactionDate, transactionType, transactionAmount, transactionCategory):
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

def calculateOverallStats(startDate, endDate):
    with open(DATA_FILENAME) as file:
        reader = csv.DictReader(file)
        relevantRows = []
        balance = 0
        expenditure = 0
        expenditureCount = 0
        income = 0
        incomeCount = 0
        categoryTransactionCount = {}
        categoryTransactionAmount = {}

        for row in reader:
            if Date(row[FIELDNAMES[1]]).compare(Date(startDate)) >= 0 and Date(row[FIELDNAMES[1]]).compare(Date(endDate)) <= 0:
                relevantRows.append(row)

        for row in relevantRows:
            if row[FIELDNAMES[2]] == "+":
                balance += float(row[FIELDNAMES[3]])
                income += float(row[FIELDNAMES[3]])
                incomeCount += 1
            elif row[FIELDNAMES[2]] == "-":
                balance -= float(row[FIELDNAMES[3]])
                expenditure += float(row[FIELDNAMES[3]])
                expenditureCount += 1

                if row[FIELDNAMES[4]].upper() in categoryTransactionCount:
                    categoryTransactionCount[row[FIELDNAMES[4]].upper()] += 1
                    categoryTransactionAmount[row[FIELDNAMES[4]].upper()] += float(row[FIELDNAMES[3]])
                else:
                    categoryTransactionCount[row[FIELDNAMES[4]].upper()] = 1
                    categoryTransactionAmount[row[FIELDNAMES[4]].upper()] = float(row[FIELDNAMES[3]])

    return balance, expenditure, expenditureCount, income, incomeCount, categoryTransactionCount, categoryTransactionAmount

# TODO: Finish this

# def calculatePayrollStats():
#     with open(DATA_FILENAME) as file:
#         reader = csv.DictReader(file)

#         for row in reversed(reader):
#             if row[FIELDNAMES[4]] == "PAYROLL":



        

def displayFooter(startDate, endDate):
    balance, expenditure, expenditureCount, income, incomeCount, categoryTransactionCount, categoryTransactionAmount = calculateOverallStats(startDate, endDate)
    
    # Sort categoryTransactionAmount in increasing order of total amount
    sortedCategoryTransactionAmount = {k: v for k, v in sorted(categoryTransactionAmount.items(), key=lambda item: item[1])}
    tab = '\t'

    sign = ""
    if balance < 0:
        sign = "-"

    print("\n" + 10*tab + "\b\bBalance: {}${:.2f}\n\n".format(sign, round(abs(balance), 2)))

    print(2*tab + "Balance Breakdown" + 9*tab + "Top Three Categories")

    print(2*tab + "Expenditure  : {} transactions totaling ${:.2f}".format(expenditureCount, round(abs(expenditure), 2)) 
            + 5*tab + list(sortedCategoryTransactionAmount)[-1] 
            + "\t\t: {} transactions totaling ${:.2f}".format(categoryTransactionCount[list(sortedCategoryTransactionAmount)[-1]], round(categoryTransactionAmount[list(sortedCategoryTransactionAmount)[-1]], 2)))

    print(2*tab + "Income       : {} paychecks totaling ${:.2f}".format(incomeCount, round(abs(income), 2)) + 6*tab 
            + list(sortedCategoryTransactionAmount)[-2] 
            + "\t: {} transactions totaling ${:.2f}".format(categoryTransactionCount[list(sortedCategoryTransactionAmount)[-2]], round(categoryTransactionAmount[list(sortedCategoryTransactionAmount)[-2]], 2)))

    print(2*tab + "Saved        : {:.2f}%".format((1 - (round(abs(expenditure), 2) / round(abs(income), 2))) * 100) + 9*tab
            + list(sortedCategoryTransactionAmount)[-3]
            + "\t\t: {} transactions totaling ${:.2f}".format(categoryTransactionCount[list(sortedCategoryTransactionAmount)[-3]], round(categoryTransactionAmount[list(sortedCategoryTransactionAmount)[-3]], 2)))

    print(2*tab + "Avg per day  : ${:.2f}".format(expenditure / Date(startDate).diffDays(Date(endDate))))


# TODO: Add balance for date range
def display(startDate, endDate, displayAll=False):
    with open(DATA_FILENAME) as file:
        reader = csv.DictReader(file)
        rowsToPrint = []
        tab = '\t'

        for row in reader:
            if Date(row[FIELDNAMES[1]]).compare(Date(startDate)) >= 0 and Date(row[FIELDNAMES[1]]).compare(Date(endDate)) <= 0:
                rowsToPrint.append(row)

        if len(rowsToPrint) == 0:
            if displayAll:
                print("No transactions logged yet.")
            else:
                print("No transactions found for this range.")
        else:
            print("\n\nIndex" + 4*tab + "Date" + 5*tab + "Type" + 5*tab + "Amount" + 5*tab + "Category\n")

            for row in rowsToPrint:
                print("{}".format(row[FIELDNAMES[0]]) + 4*tab + "{}".format(row[FIELDNAMES[1]]) + 4*tab + "{}".format(row[FIELDNAMES[2]]) + 5*tab + "${}".format(row[FIELDNAMES[3]]) + 5*tab + "{}".format(row[FIELDNAMES[4]]))

            displayFooter(startDate, endDate)

def getStartAndEndDates():
    startDate = input("Enter start date (MM/DD/YY): ")
    endDate = input("Enter end date (MM/DD/YY): ")

    return startDate, endDate


def printNotesHelp():
    os.system("clear")
    print("Help\n")
    print("\t-d <index>\t: Delete note at index")
    print("\t-e\t\t: Exit to menu")
    print("\t-h\t\t: Print this help page\n")

def deleteNote(idx):
    with open(NOTES_FILENAME) as file:
        lines = file.readlines()

    with open(NOTES_FILENAME, 'w') as file:
        for count, line in enumerate(lines):
            if count != idx:
                file.write(line)

def readNotes(keepOnScreen=False):
    if not keepOnScreen:
        os.system('clear')

    flag = False

    with open(NOTES_FILENAME) as file:
        for count, line in enumerate(file):
            print(str(count) + ". " + line)
            flag = True

    if not flag:
        print("No notes yet.")

def writeNotes():
    note = ""
    command = ""

    while True:
        if command == "h":
            readNotes(keepOnScreen=True)
            command = ""
        else:
            readNotes()

        note = input("\nType -h for help.\n-> ")

        if note[0] == "-":
            command = note.split(" ")[0].split("-")[1]
            if command == "e":
                break
            elif command == "h":
                printNotesHelp()
            elif command == "d":
                try:
                    deleteNote(int(note.split(" ")[1]))
                except:
                    print("Usage: -d <index>")
        else:
            with open(NOTES_FILENAME, 'a') as file:
                file.write(note + "\n")


# TODO: Set up mode - initial balance, think of more
# TODO: Presets - payroll, subscriptions
# TODO: Subscriptions tab and stats
# TODO: Add upcoming dates to display (payroll, Spotify)

# TODO: Watch JS playlist and implement visual graphs
#       Spending by category

# TODO: Paycheck usage breakdown: % of latest paycheck spent so far, paycheck spending trends

if __name__ == "__main__":

    # If the data file does not exist, create it
    if not os.path.isfile(DATA_FILENAME):
        print("Data file does not exist, creating now")
        dataInit()

    # Main event loop
    inputChoice = -1
    os.system('clear')
    while (inputChoice != 5):
        inputChoice = menu()
        
        if (inputChoice == 1):
            transactionDate, transactionType, transactionAmount, transactionCategory = getAddTransactionInput()
            addTransaction(transactionDate, transactionType, transactionAmount, transactionCategory)
        elif (inputChoice == 2):
            display("01/01/00", "12/31/99", True)
        elif (inputChoice == 3):
            startDate, endDate = getStartAndEndDates()
            display(startDate, endDate)
        elif (inputChoice == 4):
            writeNotes()
        elif (inputChoice == 5):
            print("Exiting")
            break
        else:
            print("Invalid input")