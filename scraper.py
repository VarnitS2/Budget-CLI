import csv

FILENAME = "data/accountActivityExport.csv"
TARGET_FILENAME = "data/data.csv"
FIELDNAMES = ["Date", "Description", "Withdrawals", "Deposits", "Category", "Balance"]
DATA_FIELDNAMES = ["Index", "Date", "Type", "Amount", "Category"]

datarows = []
with open(FILENAME) as file:
    reader = csv.DictReader(file)
    idx = sum(1 for row in reader if "XXXXX4128" in row[FIELDNAMES[1]] or "XXXXX7447" in row[FIELDNAMES[1]])

with open(FILENAME) as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        if "XXXXX4128" in row[FIELDNAMES[1]] or "XXXXX7447" in row[FIELDNAMES[1]]:
            if row[FIELDNAMES[3]] == "":
                transactionType = "-"
                transactionAmount = float(row[FIELDNAMES[2]].split("$")[1])
            else:
                transactionType = "+"
                transactionAmount = float(row[FIELDNAMES[3]].split("$")[1])

            if "XXXXX4128" in row[FIELDNAMES[1]]:
                transactionCategory = row[FIELDNAMES[1]].split("XXXXX4128")[1].split(" ")[1]
            elif "XXXXX7447" in row[FIELDNAMES[1]]:
                transactionCategory = row[FIELDNAMES[1]].split("XXXXX7447")[1].split(" ")[-1]

            transactionDate = row[FIELDNAMES[0]].split("20")[0] + row[FIELDNAMES[0]].split("20")[1]

            datarow = {
                DATA_FIELDNAMES[0]: idx,
                DATA_FIELDNAMES[1]: transactionDate,
                DATA_FIELDNAMES[2]: transactionType,
                DATA_FIELDNAMES[3]: transactionAmount,
                DATA_FIELDNAMES[4]: transactionCategory,
            }

            datarows.append(datarow)
            idx -= 1

datarows.reverse()

with open(TARGET_FILENAME, 'w') as file:
    writer = csv.DictWriter(file, fieldnames=DATA_FIELDNAMES)
    writer.writeheader()

    for row in datarows:
        writer.writerow(row)


        