import csv
import os
from lib.date import Date

DATA_FILENAME = "data/data.csv"
FIELDNAMES = ["Index", "Date", "Type", "Amount", "Category"]

def init():
    with open(DATA_FILENAME, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

def menu():
    print("\n")
    print("Budget".center(170))
    print("\n1. Add transaction.")
    print("2. See entire transaction history.")
    print("3. See transaction history between two dates.")
    print("4. Exit.\n")

    return int(input("Input: "))

def getAddTransactionInput():
    transactionDate = Date(input("Enter the date of the transaction (MM/DD/YY): "))
    transactionType = input("Enter the type of the transaction (+/-): ")
    transactionAmount = float(input("Enter the amount of the transaction: "))
    transactionCategory = input("Enter the category of the transaction: ")

    return transactionDate, transactionType, transactionAmount, transactionCategory

def addTransaction(transactionDate, transactionType, transactionAmount, transactionCategory):
    with open(DATA_FILENAME) as file:
        index = sum(1 for row in csv.reader(file))

    # TODO: insert record by date and not index

    with open(DATA_FILENAME, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        writer.writerow({
            FIELDNAMES[0]: index,
            FIELDNAMES[1]: transactionDate,
            FIELDNAMES[2]: transactionType,
            FIELDNAMES[3]: transactionAmount,
            FIELDNAMES[4]: transactionCategory
        })

def calculateOverallStats():
    with open(DATA_FILENAME) as file:
        reader = csv.DictReader(file)
        balance = 0
        expenditure = 0
        expenditureCount = 0
        income = 0
        incomeCount = 0
        categoryList = {}

        for row in reader:
            if row[FIELDNAMES[2]] == "+":
                balance += float(row[FIELDNAMES[3]])
                income += float(row[FIELDNAMES[3]])
                incomeCount += 1
            elif row[FIELDNAMES[2]] == "-":
                balance -= float(row[FIELDNAMES[3]])
                expenditure += float(row[FIELDNAMES[3]])
                expenditureCount += 1

            if row[FIELDNAMES[4]] in categoryList:
                categoryList[row[FIELDNAMES[4]]] += 1
            else:
                categoryList[row[FIELDNAMES[4]]] = 1

    # TODO: Add amount spent along with categories

    return balance, expenditure, expenditureCount, income, incomeCount, categoryList

def display(startDate, endDate, displayAll=False):
    with open(DATA_FILENAME) as file:
        reader = csv.DictReader(file)
        rowsToPrint = []
        balance, expenditure, expenditureCount, income, incomeCount, categoryList = calculateOverallStats()
        sortedCategoryList = {k: v for k, v in sorted(categoryList.items(), key=lambda item: item[1])}
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
            
            sign = ""
            if balance < 0:
                sign = "-"

            print("\n" + 10*tab + "Balance: {}${:.2f}\n\n".format(sign, round(abs(balance), 2)))

            print(2*tab + "Balance Breakdown" + 11*tab + "Top Three Categories")
            print(2*tab + "Expenditure: {} transactions totaling ${:.2f}".format(expenditureCount, round(abs(expenditure), 2)) + 8*tab + list(sortedCategoryList)[-1])
            print(2*tab + "Income:      {} paychecks totaling ${:.2f}".format(incomeCount, round(abs(income), 2)) + 8*tab + list(sortedCategoryList)[-2])
            print(15*tab + list(sortedCategoryList)[-3])

def getStartAndEndDates():
    startDate = input("Enter start date (MM/DD/YY): ")
    endDate = input("Enter end date (MM/DD/YY): ")

    return startDate, endDate


if __name__ == "__main__":

    # If the data file does not exist, create it
    if not os.path.isfile(DATA_FILENAME):
        print("Data file does not exist, creating now")
        init()

    # Main event loop
    inputChoice = -1
    os.system('clear')
    while(inputChoice != 4):
        inputChoice = menu()
        
        if (inputChoice == 1):
            transactionDate, transactionType, transactionAmount, transactionCategory = getAddTransactionInput()
            addTransaction(transactionDate, transactionType, transactionAmount, transactionCategory)
        elif (inputChoice == 2):
            display("00/00/00", "12/31/99", True)
        elif (inputChoice == 3):
            startDate, endDate = getStartAndEndDates()
            display(startDate, endDate) 
        elif (inputChoice == 4):
            print("Exiting")
            break
        else:
            print("Invalid input")