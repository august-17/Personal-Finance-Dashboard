import os

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education", "Healthcare", "Entertainment"]

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

COLUMNS = ("ID", "Date", "Type", "Category", "Amount", "Description")

SORTABLE_COLUMNS = ("Date", "Amount", "Category")

EXPORT_FORMATS = ["CSV", "PDF", "Excel"]

CSV_HEADERS = list(COLUMNS)

CUSTOM_CATEGORY = "Other"

BASE_DIR = os.path.dirname(__file__)

DATA_DIR = os.path.join(BASE_DIR, "data")

CSV_FILE = os.path.join(DATA_DIR, "transactions.csv")
BACKUP_FILE = os.path.join(DATA_DIR, "backup_transactions.csv")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.txt")
CATEGORY_BUDGET_FILE = os.path.join(DATA_DIR, "category_budget.json")

MIN_AMOUNT = 1
MAX_AMOUNT = 10_000_000

MAX_CATEGORY_LENGTH = 30

MAX_DESCRIPTION_LENGTH = 50

MIN_PIE_PERCENTAGE = 2.0

LABEL_FONT = ("Arial", 12, "bold")
TITLE_FONT = ("Arial", 18, "bold")
REPORT_FONT = ("Courier New", 11)

WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 850

REPORT_WIDTH = 850
REPORT_HEIGHT = 450

BUDGET_WIDTH = 500
BUDGET_HEIGHT = 550

EXPORT_WIDTH = 300
EXPORT_HEIGHT = 150

SELECTOR_WIDTH = 300
SELECTOR_HEIGHT = 180

EVEN_ROW_COLOR = "#f5f5f5"
ODD_ROW_COLOR = "white"