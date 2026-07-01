def shortcut_add(event=None):
    add_transaction()

def shortcut_save(event=None):
    save_changes()

def shortcut_delete(event=None):
    delete_transaction()

def shortcut_undo(event=None):
    undo_delete()

def shortcut_edit(event=None):
    edit_transaction()

def shortcut_search(event=None):
    search_entry.focus_set()

def shortcut_clear(event=None):
    clear_inputs()

def handle_category_change(event):

    if category_combobox.get() == "Other":

        custom_category_label.grid(row=5, column=0, padx=5, pady=5)
        custom_category_entry.grid(row=5, column=1, padx=5, pady=5)

    else:

        custom_category_label.grid_remove()
        custom_category_entry.grid_remove()



def clear_inputs():

    amount_entry.delete(0, tk.END)

    description_entry.delete(0, tk.END)

    custom_category_entry.delete(0, tk.END)

    category_combobox.current(0)

    custom_category_label.grid_remove()
    custom_category_entry.grid_remove()

    date_entry.set_date(datetime.now())

    type_combobox.current(0)



def enable_mousewheel_scrolling(widget):

    def _on_mousewheel(event):

        widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

    widget.bind("<Enter>", lambda e: widget.bind_all("<MouseWheel>", _on_mousewheel))

    widget.bind("<Leave>", lambda e: widget.unbind_all("<MouseWheel>"))


def insert_row(values):

    row_count = len(tree.get_children())

    tag = "evenrow" if row_count % 2 == 0 else "oddrow"

    tree.insert("", "end", values=values, tags=(tag,))


def debounce_search(event=None):

    global search_after_id

    if search_after_id is not None:

        root.after_cancel(search_after_id)

    search_after_id = root.after(250, apply_filter)

def update_sort_headers():

    sortable_columns = ("Date", "Amount", "Category")

    for column in columns:

        heading = column

        if column == sort_column:

            if sort_reverse.get(column, False):

                heading = f"{column} ▼"

            else:

                heading = f"{column} ▲"

        if column in sortable_columns:

            tree.heading(
                column,
                text=heading,
                command=lambda c=column: sort_treeview(c)
            )

        else:

            tree.heading(
                column,
                text=heading
            )



def sort_treeview(column, toggle=True):

    global sort_column

    if toggle:

        if sort_column == column:

            sort_reverse[column] = not sort_reverse.get(column, False)

        else:

            sort_column = column

            sort_reverse.setdefault(column, False)

    else:

        sort_column = column

    data = []

    for item in tree.get_children():

        values = tree.item(item)["values"]

        data.append((values, item))

    if column == "Amount":

        data.sort(
            key=lambda x: float(x[0][4]),
            reverse=sort_reverse.get(column, False)
        )

    elif column == "Date":

        data.sort(
            key=lambda x: datetime.strptime(x[0][1], "%Y-%m-%d"),
            reverse=sort_reverse.get(column, False)
        )

    elif column == "Category":

        data.sort(
            key=lambda x: x[0][3].lower(),
            reverse=sort_reverse.get(column, False)
        )

    else:

        return

    for index, (_, item) in enumerate(data):

        tree.move(item, "", index)

    update_sort_headers()

