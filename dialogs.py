import tkinter as tk
from tkinter import ttk
from datetime import datetime

from constants import (
    MONTHS, 
    EXPORT_FORMATS, 
    SELECTOR_WIDTH, 
    SELECTOR_HEIGHT, 
    EXPORT_WIDTH, 
    EXPORT_HEIGHT
)

from storage import get_available_years



def open_month_selector(root, button_text, callback):

    selector = tk.Toplevel(root)

    selector.title("Select Month")

    selector.geometry(f"{SELECTOR_WIDTH}x{SELECTOR_HEIGHT}")

    selector.resizable(False, False)

    tk.Label(selector, text="Month").pack(pady=(15, 5))

    month_combobox = ttk.Combobox(
        selector,
        values=MONTHS,
        state="readonly",
        width=20
    )

    month_combobox.current(datetime.now().month - 1)

    month_combobox.pack()

    tk.Label(selector, text="Year").pack(pady=(10, 5))

    available_years = get_available_years()

    year_combobox = ttk.Combobox(
        selector,
        values=available_years,
        state="readonly",
        width=20
    )

    year_combobox.set(str(datetime.now().year))

    year_combobox.pack()

    tk.Button(
        selector,
        text=button_text,
        command=lambda: callback(
            selector,
            month_combobox.get(),
            year_combobox.get()
        )
    ).pack(pady=15)


def get_selected_month(month_name, year):

    month_number = datetime.strptime(month_name, "%B").month

    return f"{year}-{month_number:02d}"


def open_export_window(root, selector, month, year, export_callback):

    selected_month = f"{year}-{datetime.strptime(month, '%B').month:02d}"

    export_window = tk.Toplevel(root)

    selector.destroy()

    export_window.title("Export Financial Report")

    export_window.geometry(f"{EXPORT_WIDTH}x{EXPORT_HEIGHT}")

    export_window.resizable(False, False)

    tk.Label(export_window, text="Select Export Format").pack(pady=(20, 10))

    format_combobox = ttk.Combobox(
        export_window,
        values=EXPORT_FORMATS,
        state="readonly",
        width=20
    )

    format_combobox.pack()

    format_combobox.current(0)

    tk.Button(
        export_window,
        text="Export",
        command=lambda: export_callback(
            format_combobox,
            export_window,
            selected_month
        )
    ).pack(pady=20)