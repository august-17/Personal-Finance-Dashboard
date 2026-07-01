import csv
import os
import shutil
from datetime import datetime

from constants import *


def create_csv_file():

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(CSV_HEADERS)


def create_backup():

    if os.path.exists(CSV_FILE):

        shutil.copy(CSV_FILE, BACKUP_FILE)


def read_transactions():

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        return list(csv.DictReader(file))
    

def get_all_categories():

    categories = set(CATEGORIES)

    transactions = read_transactions()

    for row in transactions:
        categories.add(row["Category"])

    return sorted(categories)


def get_next_id():

    highest_id = 0

    transactions = read_transactions()

    for row in transactions:

        current_id = int(row["ID"])

        if current_id > highest_id:

            highest_id = current_id

    return highest_id + 1


def get_available_years():

    years = set()

    transactions = read_transactions()

    for row in transactions:

        years.add(row["Date"][:4])

    years.add(str(datetime.now().year))

    return sorted(years)