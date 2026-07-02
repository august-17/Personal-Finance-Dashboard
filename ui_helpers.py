def enable_mousewheel_scrolling(widget):

    def _on_mousewheel(event):

        widget.yview_scroll(int(-1 * (event.delta / 120)), "units")

    widget.bind("<Enter>", lambda e: widget.bind_all("<MouseWheel>", _on_mousewheel))

    widget.bind("<Leave>", lambda e: widget.unbind_all("<MouseWheel>"))


def insert_row(tree, values):

    row_count = len(tree.get_children())

    tag = "evenrow" if row_count % 2 == 0 else "oddrow"

    tree.insert("", "end", values=values, tags=(tag,))