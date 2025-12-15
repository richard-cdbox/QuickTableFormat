#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Richard Sitányi (richard@cdbox.sk)
File: QuickTableFormat.py
Version: 1.0
Date: 12/15/2025
"""


import sys
import tkinter as tk
from tkinter import ttk, messagebox

try:
    import scribus
except ImportError:
    print("This script must be run from inside Scribus.")
    sys.exit(1)

# =============================================================================
# REQUIRE OPEN DOCUMENT AND SELECT ONE TABLE FRAME
# =============================================================================
if scribus.haveDoc() == 0:
    scribus.messageBox("Warning", "You should open at least one document.", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)

if scribus.selectionCount() == 0:
    scribus.messageBox("Warning", "You should select a table frame.", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)
elif scribus.selectionCount() > 1:
    scribus.messageBox("Warning", "You should select one table frame.", scribus.ICON_WARNING, scribus.BUTTON_OK)
    sys.exit(1)
elif scribus.selectionCount() == 1:
    obj = scribus.getSelectedObject()
    if scribus.getObjectType(obj) != "Table":
        scribus.messageBox("Warning", "You should select a table frame.", scribus.ICON_WARNING, scribus.BUTTON_OK)
        sys.exit(1)

# =============================================================================
# MESSAGEBOX HELPERS
# =============================================================================

def tk_info(parent, title, message):
    messagebox.showinfo(title, message, parent=parent)

def tk_warning(parent, title, message):
    messagebox.showwarning(title, message, parent=parent)

# =============================================================================
# HELPERS
# =============================================================================
lines = {"LINE_SOLID":1, "LINE_DASH":2, "LINE_DOT":3, "LINE_DASHDOT":4, "LINE_DASHDOTDOT":5}

def float_range(start, stop, step):
    while start < stop:
        yield start
        start += step

def get_all_colors_with_none():
    all_colors = ["None"]
    for i in scribus.getColorNames():
        all_colors.append(i)
    return all_colors

def get_all_rows_columns():
    trows = scribus.getTableRows(obj)
    tcolumns = scribus.getTableColumns(obj)
    rows_columns = []
    for r in range(trows):
        for c in range(tcolumns):
            rows_columns.append([r, c])
    return rows_columns

def get_keys_from_lines():
    keys = []
    for k in lines:
        keys.append(k[5:])
    return keys

# =============================================================================
# DIALOG
# =============================================================================
def create_dialog(root=None):
    root.title("Quick table format")
    root.geometry("400x700")
    root.resizable(False, False)
    root.grab_set()
    root.attributes("-topmost", True)

    # Cell padding
    ttk.Label(root, text="Cell padding:").place(x=20,y=20)
    paddCombo = ttk.Combobox(root, width=5, state="readonly")
    paddCombo["values"] = list(range(1, 21, 1))
    paddCombo.place(x=130,y=20)
    paddCombo.current(0)
    ttk.Separator(orient="horizontal")

    def update_cell_padding():
        padding = int(paddCombo.get())
        for i in get_all_rows_columns():
            r = i[0]
            c = i[1]
            scribus.setCellLeftPadding(r, c, padding, obj)
            scribus.setCellTopPadding(r, c, padding, obj)
            scribus.setCellRightPadding(r, c, padding, obj)
            scribus.setCellBottomPadding(r, c, padding, obj)

    def update_cell_padding_info():
        try:
            update_cell_padding()
            tk_info(root, "Update cell padding", "The update was successful.")
        except:
            tk_warning(root, "Update cell padding", "The update was not successful.")

    ttk.Button(root, text="Update cell padding", command=update_cell_padding_info).place(x=20, y=60)

    # Table color
    ttk.Label(root, text="Table color:").place(x=20,y=100)
    tb_colorCombo = ttk.Combobox(root, width=20, state="readonly")
    tb_colorCombo["values"] = get_all_colors_with_none()
    tb_colorCombo.place(x=130,y=100)
    tb_colorCombo.current(0)

    def update_table_color():
        table_color = tb_colorCombo.get()
        scribus.setTableFillColor(table_color, obj)

    def update_table_color_info():
        try:
            update_table_color()
            tk_info(root, "Update table color", "The update was successful.")
        except:
            tk_warning(root, "Update table color", "The update was not successful.")

    ttk.Button(root, text="Update table color", command=update_table_color_info).place(x=20, y=140)

    # Table border
    ttk.Label(root, text="Table border").place(x=20,y=180)
    ttk.Label(root, text="Border width:").place(x=40,y=200)
    tbwCombo = ttk.Combobox(root, width=5, state="readonly")
    tbwCombo["values"] = list(float_range(0.25, 21, 0.25))
    tbwCombo.place(x=130,y=200)
    tbwCombo.current(3)
    ttk.Label(root, text="Border style:").place(x=40,y=240)
    tbsCombo = ttk.Combobox(root, width=20, state="readonly")
    tbsCombo["values"] = get_keys_from_lines()
    tbsCombo.place(x=130,y=240)
    tbsCombo.current(0)
    ttk.Label(root, text="Border color:").place(x=40,y=280)
    tbcCombo = ttk.Combobox(root, width=20, state="readonly")
    tbcCombo["values"] = get_all_colors_with_none()
    tbcCombo.place(x=130,y=280)
    tbcCombo.current(1)
    ttk.Label(root, text="Shade:").place(x=40,y=320)
    tbsh_var = tk.IntVar(value=100)
    tbshSlider = ttk.Scale(root, from_=0, to=100, orient="horizontal", variable=tbsh_var)
    tbshSlider.place(x=130, y=320, width=150)
    tbshLabel = ttk.Label(root, text="100 %")
    tbshLabel.place(x=290, y=320)

    def update_tbsh_label(*args):
        tbshLabel.config(text=f"{tbsh_var.get()} %")
    tbsh_var.trace_add("write", update_tbsh_label)

    def update_table_border():
        tbwidth = float(tbwCombo.get())
        tbstyle = lines["LINE_"+tbsCombo.get()]
        tbcolor = tbcCombo.get()
        tbshade = int(tbsh_var.get())
        tbborder_param = [(tbwidth, tbstyle, tbcolor, tbshade)]
        scribus.setTableLeftBorder(tbborder_param, obj)
        scribus.setTableTopBorder(tbborder_param, obj)
        scribus.setTableRightBorder(tbborder_param, obj)
        scribus.setTableBottomBorder(tbborder_param, obj)

    def update_table_border_info():
        try:
            update_table_border()
            tk_info(root, "Update table border", "The update was successful.")
        except:
            tk_warning(root, "Update table border", "The update was not successful.")

    ttk.Button(root, text="Update table border", command=update_table_border_info).place(x=20, y=360)

    # Cell border
    ttk.Label(root, text="Cell border").place(x=20,y=400)
    ttk.Label(root, text="Border width:").place(x=40,y=420)
    cwCombo = ttk.Combobox(root, width=5, state="readonly")
    cwCombo["values"] = list(float_range(0.25, 21, 0.25))
    cwCombo.place(x=130,y=420)
    cwCombo.current(3)
    ttk.Label(root, text="Border style:").place(x=40,y=460)
    csCombo = ttk.Combobox(root, width=20, state="readonly")
    csCombo["values"] = get_keys_from_lines()
    csCombo.place(x=130,y=460)
    csCombo.current(0)
    ttk.Label(root, text="Border color:").place(x=40,y=500)
    ccCombo = ttk.Combobox(root, width=20, state="readonly")
    ccCombo["values"] = get_all_colors_with_none()
    ccCombo.place(x=130,y=500)
    ccCombo.current(1)
    ttk.Label(root, text="Shade:").place(x=40,y=540)
    csh_var = tk.IntVar(value=100)
    cshSlider = ttk.Scale(root, from_=0, to=100, orient="horizontal", variable=csh_var)
    cshSlider.place(x=130, y=540, width=150)
    cshLabel = ttk.Label(root, text="100 %")
    cshLabel.place(x=290, y=540)

    def update_csh_label(*args):
        cshLabel.config(text=f"{csh_var.get()} %")
    csh_var.trace_add("write", update_csh_label)

    def update_cell_border():
        cwidth = float(cwCombo.get())
        cstyle = lines["LINE_"+csCombo.get()]
        ccolor = ccCombo.get()
        cshade = int(csh_var.get())
        cborder_param = [(cwidth, cstyle, ccolor, cshade)]
        for i in get_all_rows_columns():
            r = i[0]
            c = i[1]
            scribus.setCellLeftBorder(r, c, cborder_param, obj)
            scribus.setCellTopBorder(r, c, cborder_param, obj)
            scribus.setCellRightBorder(r, c, cborder_param, obj)
            scribus.setCellBottomBorder(r, c, cborder_param, obj)

    def update_cell_border_info():
        try:
            update_cell_border()
            tk_info(root, "Update cell border", "The update was successful.")
        except:
            tk_warning(root, "Update cell border", "The update was not successful.")

    ttk.Button(root, text="Update cell border", command=update_cell_border_info).place(x=20, y=580)

    def update_all():
        update_cell_padding()
        update_table_color()
        update_table_border()
        update_cell_border()

    def update_all_info():
        try:
            update_all()
            tk_info(root, "Update all", "The update was successful.")
        except:
            tk_warning(root, "Update all", "The update was not successful.")

    def close_dialog():
        root.destroy()
        sys.exit(1)

    ttk.Button(root, text="Close", command=close_dialog).place(x=20, y=650)
    ttk.Button(root, text="Update all", command=update_all_info).place(x=110, y=650)

# =============================================================================
# MAIN
# =============================================================================
def main(argv):
    root=tk.Tk()
    create_dialog(root)
    root.mainloop()

def main_wrapper(argv):
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        if scribus.haveDoc():
            scribus.setRedraw(True)
            scribus.redrawAll()
        scribus.statusMessage("Script finished.")
        scribus.progressReset()

if __name__=="__main__":
    main_wrapper(sys.argv)
