import os

CATEGORIES = ["Food", "Travel", "Shopping", "Bills", "Education", "Healthcare", "Entertainment"]

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

COLUMNS = ("ID", "Date", "Type", "Category", "Amount", "Description")

SORTABLE_COLUMNS = ("Date", "Amount", "Category")

EXPORT_FORMATS = ["CSV", "PDF", "Excel"]

CSV_HEADERS = list(COLUMNS)

CUSTOM_CATEGORY = "Other"

CSV_FILE = os.path.join(os.path.dirname(__file__), "transactions.csv")

BUDGET_FILE = os.path.join(os.path.dirname(__file__), "budget.txt")

CATEGORY_BUDGET_FILE = os.path.join(os.path.dirname(__file__), "category_budget.json")

BACKUP_FILE = os.path.join(os.path.dirname(__file__), "backup_transactions.csv")

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