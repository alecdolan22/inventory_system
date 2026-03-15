import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import uuid

# Connect to database
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Drop old tables if needed (run once to reset)
cursor.execute("DROP TABLE IF EXISTS inventory")
cursor.execute("DROP TABLE IF EXISTS sold")
cursor.execute("DROP TABLE IF EXISTS dates")

# Create tables with 'id' as PRIMARY KEY AUTOINCREMENT
cursor.execute('''
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT,
    item TEXT,
    vendor TEXT,
    price REAL,
    quantity INTEGER,
    date_sold TEXT,
    taxable TEXT
)
''')

cursor.execute('''
CREATE TABLE sold (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT,
    item TEXT,
    vendor TEXT,
    price REAL,
    quantity INTEGER,
    date_sold TEXT,
    taxable TEXT
)
''')

cursor.execute('''
CREATE TABLE dates (
    date TEXT PRIMARY KEY
)
''')

conn.commit()

root = tk.Tk()
root.title("Inventory Management System")
root.configure(bg="#f0f0f0")  # Light gray background

# Configure root grid weights for centering
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# White header (40 pixels deep)
header_frame = tk.Frame(root, bg="white", height=40)
header_frame.grid(row=0, column=0, columnspan=5, sticky="ew")
header_frame.grid_propagate(False)  # Prevent frame from shrinking

# Centered placeholder text in header
header_label = tk.Label(header_frame, text="placeholder", bg="white", fg="black", font=("Arial", 16, "bold"))
header_label.place(relx=0.5, rely=0.5, anchor="center")

# Main container for top section (moved down)
top_frame = tk.Frame(root, bg="#f0f0f0")
top_frame.grid(row=1, column=0, columnspan=5, sticky="ew", padx=10, pady=10)

# Input fields container
input_container = tk.Frame(top_frame, bg="#f0f0f0")
input_container.grid(row=0, column=0, columnspan=3, sticky="ew")

fields = ["ID", "Item", "Vendor", "Price", "Quantity", "Taxable", "Year", "Month", "Day"]
entries = {}

# Arrange fields in rows of 3 for even spacing
for i, field in enumerate(fields):
    row = i // 3
    col = (i % 3) * 2
    
    label = tk.Label(input_container, text=field, bg="#f0f0f0", fg="black")
    label.grid(row=row, column=col, sticky="e", padx=5, pady=2)
    
    if field == "Taxable":
        var = tk.StringVar(value="No")
        option = tk.OptionMenu(input_container, var, "Yes", "No")
        option.grid(row=row, column=col+1, padx=5, pady=2, sticky="w")
        entries[field] = var
    else:
        entry = tk.Entry(input_container, width=15, bg="white", fg="black", highlightbackground="black", highlightthickness=1)
        entry.grid(row=row, column=col+1, padx=5, pady=2, sticky="w")
        
        # Add placeholder text and color behavior for date fields in main input
        if field == "Year":
            entry.insert(0, "YYYY")
            entry.config(fg="gray")
            entry.bind("<FocusIn>", lambda e: clear_placeholder(entry, "YYYY"))
            entry.bind("<FocusOut>", lambda e: restore_placeholder(entry, "YYYY"))
            entry.bind("<Key>", lambda e: entry.config(fg="black"))
        elif field == "Month":
            entry.insert(0, "MM")
            entry.config(fg="gray")
            entry.bind("<FocusIn>", lambda e: clear_placeholder(entry, "MM"))
            entry.bind("<FocusOut>", lambda e: restore_placeholder(entry, "MM"))
            entry.bind("<Key>", lambda e: entry.config(fg="black"))
        elif field == "Day":
            entry.insert(0, "DD")
            entry.config(fg="gray")
            entry.bind("<FocusIn>", lambda e: clear_placeholder(entry, "DD"))
            entry.bind("<FocusOut>", lambda e: restore_placeholder(entry, "DD"))
            entry.bind("<Key>", lambda e: entry.config(fg="black"))
        
        entries[field] = entry

# Date filter container
filter_frame = tk.Frame(top_frame, bg="#f0f0f0")
filter_frame.grid(row=0, column=3, columnspan=2, padx=10, pady=5, sticky="n")

tk.Label(filter_frame, text="Filter Inventory by Date (YYYY-MM-DD)", bg="#f0f0f0", fg="black").grid(row=0, column=0, columnspan=2)
tk.Label(filter_frame, text="Year", bg="#f0f0f0", fg="black").grid(row=1, column=0)
year_var = tk.StringVar()
year_entry = tk.Entry(filter_frame, textvariable=year_var, width=6, bg="white", fg="black", highlightbackground="black", highlightthickness=1)
year_entry.grid(row=1, column=1)
year_entry.insert(0, "YYYY")
year_entry.config(fg="gray")
year_entry.bind("<FocusIn>", lambda e: clear_placeholder(year_entry, "YYYY"))
year_entry.bind("<FocusOut>", lambda e: restore_placeholder(year_entry, "YYYY"))
year_entry.bind("<Key>", lambda e: year_entry.config(fg="black"))

tk.Label(filter_frame, text="Month", bg="#f0f0f0", fg="black").grid(row=2, column=0)
month_var = tk.StringVar()
month_entry = tk.Entry(filter_frame, textvariable=month_var, width=6, bg="white", fg="black", highlightbackground="black", highlightthickness=1)
month_entry.grid(row=2, column=1)
month_entry.insert(0, "MM")
month_entry.config(fg="gray")
month_entry.bind("<FocusIn>", lambda e: clear_placeholder(month_entry, "MM"))
month_entry.bind("<FocusOut>", lambda e: restore_placeholder(month_entry, "MM"))
month_entry.bind("<Key>", lambda e: month_entry.config(fg="black"))

tk.Label(filter_frame, text="Day", bg="#f0f0f0", fg="black").grid(row=3, column=0)
day_var = tk.StringVar()
day_entry = tk.Entry(filter_frame, textvariable=day_var, width=6, bg="white", fg="black", highlightbackground="black", highlightthickness=1)
day_entry.grid(row=3, column=1)
day_entry.insert(0, "DD")
day_entry.config(fg="gray")
day_entry.bind("<FocusIn>", lambda e: clear_placeholder(day_entry, "DD"))
day_entry.bind("<FocusOut>", lambda e: restore_placeholder(day_entry, "DD"))
day_entry.bind("<Key>", lambda e: day_entry.config(fg="black"))

# Tables & labels (moved down)
tk.Label(root, text="Inventory", bg="#f0f0f0", fg="black", font=("Arial", 12, "bold")).grid(row=2, column=0, columnspan=3, pady=(10, 5))
inventory_listbox = tk.Listbox(root, width=75, height=20, bg="white", fg="black", highlightbackground="black", highlightthickness=1)
inventory_listbox.grid(row=3, column=0, columnspan=3, padx=10, sticky="ew")

tk.Label(root, text="Sold Items", bg="#f0f0f0", fg="black", font=("Arial", 12, "bold")).grid(row=2, column=3, columnspan=2, pady=(10, 5))
sold_listbox = tk.Listbox(root, width=75, height=20, bg="white", fg="black", highlightbackground="black", highlightthickness=1)
sold_listbox.grid(row=3, column=3, columnspan=2, padx=10, sticky="ew")

def generate_item_id():
    return str(uuid.uuid4())[:8]

def add_item():
    try:
        item_id = entries["ID"].get().strip()
        if not item_id:
            item_id = generate_item_id()
        item = entries["Item"].get().strip()
        vendor = entries["Vendor"].get().strip()
        price = float(entries["Price"].get().strip())
        quantity = int(entries["Quantity"].get().strip())
        taxable = entries["Taxable"].get()

        year = entries["Year"].get().strip()
        month = entries["Month"].get().strip()
        day = entries["Day"].get().strip()

        if not item or not vendor:
            messagebox.showwarning("Missing Fields", "Item and Vendor are required.")
            return

        if year and month and day:
            date_sold = f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            date_sold = datetime.now().strftime("%Y-%m-%d")

        # Show confirmation dialog
        confirm_message = f"Add the following item to inventory?\n\n"
        confirm_message += f"Item: {item}\n"
        confirm_message += f"Vendor: {vendor}\n"
        confirm_message += f"Price: ${price}\n"
        confirm_message += f"Quantity: {quantity}\n"
        confirm_message += f"Taxable: {taxable}\n"
        confirm_message += f"Date: {date_sold}"
        
        if messagebox.askyesno("Confirm Add Item", confirm_message):
            cursor.execute(
                "INSERT INTO inventory (item_id, item, vendor, price, quantity, date_sold, taxable) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (item_id, item, vendor, price, quantity, date_sold, taxable)
            )
            cursor.execute("INSERT OR IGNORE INTO dates (date) VALUES (?)", (date_sold,))
            conn.commit()
            view_items()
            clear_all_entries()
            messagebox.showinfo("Success", "Item added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add item: {e}")

def clear_placeholder(entry, placeholder_text):
    """Clear placeholder text when field gets focus"""
    current_text = entry.get()
    if current_text == placeholder_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def restore_placeholder(entry, placeholder_text):
    """Restore placeholder text when field loses focus and is empty"""
    current_text = entry.get().strip()
    if not current_text:
        entry.insert(0, placeholder_text)
        entry.config(fg="gray")

def clear_all_entries():
    """Clear all input fields"""
    for field in entries:
        if field == "Taxable":
            entries[field].set("No")
        else:
            entries[field].delete(0, tk.END)
            # Restore placeholder text for date fields
            if field == "Year":
                entries[field].insert(0, "YYYY")
                entries[field].config(fg="gray")
            elif field == "Month":
                entries[field].insert(0, "MM")
                entries[field].config(fg="gray")
            elif field == "Day":
                entries[field].insert(0, "DD")
                entries[field].config(fg="gray")

def get_selected_id(listbox):
    try:
        idx = listbox.curselection()[0]
        text = listbox.get(idx)
        start = text.index("[DBID: ") + 7
        end = text.index("]", start)
        return int(text[start:end])
    except Exception:
        return None

def load_selected_inventory(event=None):
    record_id = get_selected_id(inventory_listbox)
    if record_id is None:
        return
    cursor.execute("SELECT item_id, item, vendor, price, quantity, taxable, date_sold FROM inventory WHERE id=?", (record_id,))
    row = cursor.fetchone()
    if row:
        entries["ID"].delete(0, tk.END)
        entries["ID"].insert(0, row[0])
        entries["Item"].delete(0, tk.END)
        entries["Item"].insert(0, row[1])
        entries["Vendor"].delete(0, tk.END)
        entries["Vendor"].insert(0, row[2])
        entries["Price"].delete(0, tk.END)
        entries["Price"].insert(0, str(row[3]))
        entries["Quantity"].delete(0, tk.END)
        entries["Quantity"].insert(0, str(row[4]))
        entries["Taxable"].set(row[5])  # Taxable is StringVar

        # Parse date_sold into Year, Month, Day
        if row[6]:
            parts = row[6].split("-")
            if len(parts) == 3:
                entries["Year"].delete(0, tk.END)
                entries["Year"].insert(0, parts[0])
                entries["Month"].delete(0, tk.END)
                entries["Month"].insert(0, parts[1])
                entries["Day"].delete(0, tk.END)
                entries["Day"].insert(0, parts[2])

def update_item():
    record_id = get_selected_id(inventory_listbox)
    if record_id is None:
        messagebox.showinfo("Info", "Please select an item in Inventory to update.")
        return
    try:
        item_id = entries["ID"].get().strip()
        item = entries["Item"].get().strip()
        vendor = entries["Vendor"].get().strip()
        price = float(entries["Price"].get().strip())
        quantity = int(entries["Quantity"].get().strip())
        taxable = entries["Taxable"].get()

        year = entries["Year"].get().strip()
        month = entries["Month"].get().strip()
        day = entries["Day"].get().strip()

        if not item or not vendor:
            messagebox.showwarning("Missing Fields", "Item and Vendor are required.")
            return

        if year and month and day:
            date_sold = f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"
        else:
            date_sold = datetime.now().strftime("%Y-%m-%d")

        cursor.execute(
            "UPDATE inventory SET item_id=?, item=?, vendor=?, price=?, quantity=?, taxable=?, date_sold=? WHERE id=?",
            (item_id, item, vendor, price, quantity, taxable, date_sold, record_id)
        )
        cursor.execute("INSERT OR IGNORE INTO dates (date) VALUES (?)", (date_sold,))
        conn.commit()
        view_items()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update item: {e}")

def delete_item(table="inventory"):
    lb = inventory_listbox if table == "inventory" else sold_listbox
    record_id = get_selected_id(lb)
    if record_id is None:
        messagebox.showinfo("Info", f"Please select an item in {table.capitalize()} to delete.")
        return
    try:
        cursor.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
        conn.commit()
        view_items()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete item: {e}")

def mark_as_sold():
    record_id = get_selected_id(inventory_listbox)
    if record_id is None:
        messagebox.showinfo("Info", "Please select an item in Inventory to mark as Sold.")
        return
    try:
        cursor.execute("SELECT item_id, item, vendor, price, quantity, date_sold, taxable FROM inventory WHERE id=?", (record_id,))
        inventory_item = cursor.fetchone()
        if not inventory_item: 
            messagebox.showerror("Error", "Item not found in inventory.")
            return
        
        item_id, item, vendor, price, quantity, date_sold, taxable = inventory_item
        
        if quantity <= 0:
            messagebox.showwarning("Warning", "Item quantity is 0. Cannot sell.")
            return
        
        # Create a new sold entry with quantity 1
        cursor.execute("INSERT INTO sold (item_id, item, vendor, price, quantity, date_sold, taxable) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                    (item_id, item, vendor, price, 1, date_sold, taxable))
        
        # Always keep a copy in inventory, decrement quantity by 1
        if quantity - 1 == 0:
            cursor.execute("UPDATE inventory SET quantity = 0 WHERE id=?", (record_id,))
            messagebox.showinfo("Success", f"Sold last {item}. Item kept in inventory with quantity 0.")
        else:
            cursor.execute("UPDATE inventory SET quantity = quantity - 1 WHERE id=?", (record_id,))
            messagebox.showinfo("Success", f"Sold 1 {item}. Inventory: {quantity-1} remaining.")
        
        conn.commit()
        view_items()
        update_button_states()
        
    except Exception as e: 
        messagebox.showerror("Error", f"Failed to mark as sold: {e}")

def mark_as_forsale():
    record_id = get_selected_id(sold_listbox)
    if record_id is None:
        messagebox.showinfo("Info", "Please select an item in Sold Items to mark as For Sale.")
        return
    try:
        cursor.execute("SELECT item_id, item, vendor, price, quantity, date_sold, taxable FROM sold WHERE id=?", (record_id,))
        item = cursor.fetchone()
        if item:
            cursor.execute("INSERT INTO inventory (item_id, item, vendor, price, quantity, date_sold, taxable) VALUES (?, ?, ?, ?, ?, ?, ?)", item)
            cursor.execute("DELETE FROM sold WHERE id=?", (record_id,))
            conn.commit()
            view_items()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to mark as for sale: {e}")

def view_items():
    inventory_listbox.delete(0, tk.END)
    sold_listbox.delete(0, tk.END)

    filters = []
    params = []

    if year_var.get().strip():
        filters.append("strftime('%Y', date_sold) = ?")
        params.append(year_var.get().strip())
    if month_var.get().strip():
        filters.append("strftime('%m', date_sold) = ?")
        params.append(month_var.get().zfill(2))
    if day_var.get().strip():
        filters.append("strftime('%d', date_sold) = ?")
        params.append(day_var.get().zfill(2))

    filter_clause = " AND " + " AND ".join(filters) if filters else ""

    cursor.execute(f"""
        SELECT id, item_id, item, vendor, price, quantity, taxable, date_sold
        FROM inventory
        WHERE 1=1 {filter_clause}
        ORDER BY date_sold DESC
    """, params)
    for row in cursor.fetchall():
        inventory_listbox.insert(tk.END,
            f"[DBID: {row[0]}] {row[2]} | Vendor: {row[3]} | Qty: {row[5]} | ${row[4]:.2f} | Date Created: {row[7]} | Taxable: {row[6]}")

    cursor.execute(f"""
        SELECT id, item_id, item, vendor, price, quantity, taxable, date_sold
        FROM sold
        WHERE 1=1 {filter_clause}
        ORDER BY date_sold DESC
    """, params)
    for row in cursor.fetchall():
        sold_listbox.insert(tk.END,
            f"[DBID: {row[0]}] {row[2]} | Vendor: {row[3]} | Qty: {row[5]} | ${row[4]:.2f} | Date Created: {row[7]} | Taxable: {row[6]}")

def update_button_states():
    """Update button states based on selection"""
    inventory_selected = bool(inventory_listbox.curselection())
    sold_selected = bool(sold_listbox.curselection())
    
    # Disable Mark as For Sale when inventory item is selected
    if inventory_selected and not sold_selected:
        button_widgets["Mark as For Sale"].config(state="disabled")
    else:
        button_widgets["Mark as For Sale"].config(state="normal")
    
    # Disable Mark as Sold when sold item is selected
    if sold_selected and not inventory_selected:
        button_widgets["Mark as Sold"].config(state="disabled")
    else:
        button_widgets["Mark as Sold"].config(state="normal")
    
    # Enable Mark as For Sale only when sold item is selected
    if sold_selected:
        button_widgets["Mark as For Sale"].config(state="normal")

def on_inventory_select(event=None):
    """Handle inventory listbox selection"""
    load_selected_inventory(event)
    update_button_states()

def on_sold_select(event=None):
    """Handle sold listbox selection"""
    # Clear inventory selection when sold item is selected
    inventory_listbox.selection_clear(0, tk.END)
    update_button_states()

# Bind selecting inventory list item to load its data into fields
inventory_listbox.bind('<<ListboxSelect>>', on_inventory_select)
sold_listbox.bind('<<ListboxSelect>>', on_sold_select)

# Configure bottom row for buttons
root.grid_rowconfigure(5, weight=0)

# Buttons container at bottom
button_container = tk.Frame(root, bg="#f0f0f0")
button_container.grid(row=5, column=0, columnspan=5, pady=10, sticky="ew")

buttons = [
    ("Add Item", add_item),
    ("Update Item", update_item),
    ("Mark as Sold", mark_as_sold),
    ("Mark as For Sale", mark_as_forsale),
    ("Delete Item", delete_item),
    ("Refresh View", view_items),
]

# Create button references for state management
button_widgets = {}
for idx, (text, cmd) in enumerate(buttons):
    # Configure columns for even spacing
    button_container.grid_columnconfigure(idx, weight=1)
    button_widgets[text] = tk.Button(button_container, text=text, command=cmd, width=15)
    button_widgets[text].grid(row=0, column=idx, padx=5, pady=5, sticky="ew")

view_items()
update_button_states()  # Initialize button states
root.mainloop()
