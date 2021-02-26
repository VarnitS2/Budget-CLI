import csv

FILENAME = "Data/data.csv"

def init():
    with open(FILENAME) as file:
        return csv.DictReader(file)

if __name__ == "__main__":
    reader = init()
    print(reader)