import csv
import os
import json
import shutil
from datetime import datetime

from constants import (
    CSV_FILE, 
    CSV_HEADERS, 
    CATEGORIES, 
    BUDGET_FILE, 
    CATEGORY_BUDGET_FILE, 
    BACKUP_FILE
)


def create_csv_file():

    if not os.path.exists(CSV_FILE):

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow(CSV_HEADERS)


def create_backup():

    try:

        if os.path.exists(CSV_FILE):

            shutil.copy(CSV_FILE, BACKUP_FILE)

    except OSError as e:

        pass


def read_transactions():

    create_csv_file()

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        return list(csv.DictReader(file))


def get_next_id():

    highest_id = 0

    transactions = read_transactions()

    for row in transactions:

        try:

            current_id = int(row["ID"])

        except ValueError:

            continue

        if current_id > highest_id:

            highest_id = current_id

    return highest_id + 1
    

def get_all_categories():

    categories = set(CATEGORIES)

    transactions = read_transactions()

    for row in transactions:

        categories.add(row["Category"])

    return sorted(categories)


def get_available_years():

    years = set()

    transactions = read_transactions()

    for row in transactions:

        years.add(row["Date"][:4])

    years.add(str(datetime.now().year))

    return sorted(years)


def load_budget():

    if not os.path.exists(BUDGET_FILE):

        return 0

    try:

        with open(BUDGET_FILE, "r", encoding="utf-8") as file:

            return float(file.read())

    except (ValueError, OSError):

        return 0


def write_budget(budget):

    with open(BUDGET_FILE, "w", encoding="utf-8") as file:

        file.write(str(budget))


def load_category_budgets():

    if not os.path.exists(CATEGORY_BUDGET_FILE):

        return {}

    try:

        with open(CATEGORY_BUDGET_FILE, "r", encoding="utf-8") as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {}


def save_category_budgets(category_budgets):

    with open(CATEGORY_BUDGET_FILE, "w", encoding="utf-8") as file:

        json.dump(category_budgets, file, indent=4)