import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkfont
import json
import os
from datetime import datetime
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class InventoryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("InventoryPro - Advanced Management System")
        self.root.geometry("1280x800")
        self.root.minsize(1024, 768)
        
        # Custom colors
        self.colors = {
            "primary": "#3498db",
            "secondary": "#2ecc71",
            "danger": "#e74c3c",
            "warning": "#f39c12",
            "dark": "#2c3e50",
            "light": "#ecf0f1",
            "background": "#f5f7fa"
        }
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabel", background=self.colors["background"], font=('Helvetica', 10))
        self.style.configure("TButton", font=('Helvetica', 10), padding=6)
        self.style.configure("Primary.TButton", foreground="white", background=self.colors["primary"])
        self.style.map("Primary.TButton",
            background=[('active', self.colors["primary"]), ('disabled', '#cccccc')])
        
        self.style.configure("Secondary.TButton", foreground="white", background=self.colors["secondary"])
        self.style.map("Secondary.TButton",
            background=[('active', self.colors["secondary"]), ('disabled', '#cccccc')])
        
        self.style.configure("Danger.TButton", foreground="white", background=self.colors["danger"])
        self.style.map("Danger.TButton",
            background=[('active', self.colors["danger"]), ('disabled', '#cccccc')])
        
        self.style.configure("Warning.TButton", foreground="white", background=self.colors["warning"])
        
        self.style.configure("TEntry", padding=5)
        self.style.configure("Treeview", rowheight=30, font=('Helvetica', 10))
        self.style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
        
        # Create data files if they don't exist
        self.init_data_files()
        
        self.current_user = None
        self.login_screen()

    def init_data_files(self):
        if not os.path.exists("users.json"):
            with open("users.json", "w") as f:
                json.dump({"admin": "admin123"}, f)
        
        if not os.path.exists("inventory.json"):
            sample_inventory = [
                {"id": 1, "name": "Premium Laptop", "category": "Electronics", "price": 999.99, 
                 "quantity": 15, "min_stock": 10, "description": "High-end business laptop", 
                 "last_updated": "2023-01-01 10:00:00"},
                {"id": 2, "name": "Wireless Mouse", "category": "Accessories", "price": 25.50, 
                 "quantity": 42, "min_stock": 20, "description": "Ergonomic wireless mouse", 
                 "last_updated": "2023-01-05 14:30:00"},
                {"id": 3, "name": "Monitor Stand", "category": "Furniture", "price": 45.75, 
                 "quantity": 8, "min_stock": 15, "description": "Adjustable monitor stand", 
                 "last_updated": "2023-01-10 09:15:00"}
            ]
            with open("inventory.json", "w") as f:
                json.dump(sample_inventory, f, indent=2)
        
        if not os.path.exists("transactions.json"):
            with open("transactions.json", "w") as f:
                json.dump([], f)

    def login_screen(self):
        self.clear_window()
        self.root.configure(bg=self.colors["background"])
        
        login_frame = ttk.Frame(self.root, padding=30, style="TFrame")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo placeholder
        logo_label = ttk.Label(login_frame, text="InventoryPro", font=('Helvetica', 24, 'bold'), 
                              foreground=self.colors["primary"])
        logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Form elements
        ttk.Label(login_frame, text="Username:", font=('Helvetica', 12)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = ttk.Entry(login_frame, font=('Helvetica', 12), width=25)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(login_frame, text="Password:", font=('Helvetica', 12)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = ttk.Entry(login_frame, font=('Helvetica', 12), show="•", width=25)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Login button
        login_button = ttk.Button(login_frame, text="Login", style="Primary.TButton", 
                                 command=self.authenticate)
        login_button.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # Set focus and default credentials for demo
        self.username_entry.insert(0, "admin")
        self.password_entry.insert(0, "admin123")
        self.username_entry.focus()

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        with open("users.json", "r") as f:
            users = json.load(f)
            
        if username in users and users[username] == password:
            self.current_user = username
            self.main_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password", parent=self.root)

    def main_dashboard(self):
        self.clear_window()
        
        # Configure main window layout
        self.root.configure(bg=self.colors["background"])
        
        # Header frame
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Dashboard title
        ttk.Label(header_frame, text=f"Dashboard | Welcome, {self.current_user}", 
                 font=('Helvetica', 18, 'bold'), foreground=self.colors["dark"]).pack(side="left")
        
        # Menu buttons
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill="x", padx=10, pady=5)
        
        nav_buttons = [
            ("Dashboard", self.main_dashboard),
            ("Products", self.view_products),
            ("Add Product", self.add_product),
            ("Reports", self.reports_dashboard),
            ("Logout", self.logout)
        ]
        
        for text, command in nav_buttons:
            btn = ttk.Button(menu_frame, text=text, style="Primary.TButton" if text == "Dashboard" else "TButton",
                            command=command)
            btn.pack(side="left", padx=5)
        
        # Content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Stats cards
        stats_frame = ttk.Frame(content_frame)
        stats_frame.pack(fill="x", pady=(0, 10))
        
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        stats_data = [
            {"title": "Total Products", "value": len(inventory), "color": self.colors["primary"]},
            {"title": "Inventory Value", "value": f"${sum(p['price']*p['quantity'] for p in inventory):,.2f}", 
             "color": self.colors["secondary"]},
            {"title": "Low Stock Items", "value": sum(1 for p in inventory if p['quantity'] <= p['min_stock']), 
             "color": self.colors["warning"]},
            {"title": "Categories", "value": len(set(p['category'] for p in inventory)), 
             "color": self.colors["dark"]}
        ]
        
        for stat in stats_data:
            card = ttk.Frame(stats_frame, relief="groove", borderwidth=2, padding=10)
            card.pack(side="left", fill="both", expand=True, padx=5)
            
            ttk.Label(card, text=stat["title"], font=('Helvetica', 10, 'bold'), 
                     foreground=stat["color"]).pack(anchor="w")
            ttk.Label(card, text=str(stat["value"]), font=('Helvetica', 24, 'bold')).pack()
        
        # Recent activity frame
        activity_frame = ttk.LabelFrame(content_frame, text="Recent Activity", padding=10)
        activity_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Chart frame
        chart_frame = ttk.Frame(activity_frame)
        chart_frame.pack(fill="both", expand=True, side="left")
        
        # Inventory summary chart
        fig = plt.figure(figsize=(6, 4), dpi=80)
        ax = fig.add_subplot(111)
        
        categories = {}
        for product in inventory:
            if product['category'] not in categories:
                categories[product['category']] = 0
            categories[product['category']] += product['price'] * product['quantity']
        
        labels = list(categories.keys())
        values = list(categories.values())
        explode = [0.1] + [0]*(len(labels)-1)
        
        ax.pie(values, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, explode=explode)
        ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle
        ax.set_title('Inventory Value by Category')
        
        chart = FigureCanvasTkAgg(fig, chart_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)
        
        # Recent transactions table
        trans_frame = ttk.Frame(activity_frame, width=300, padding=(10,0,0,0))
        trans_frame.pack(fill="both", expand=True, side="right")
        
        scrollbar = ttk.Scrollbar(trans_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("action", "product", "time")
        self.trans_tree = ttk.Treeview(trans_frame, columns=columns, show="headings", height=10,
                                     yscrollcommand=scrollbar.set)
        
        self.trans_tree.heading("action", text="Action")
        self.trans_tree.heading("product", text="Product")
        self.trans_tree.heading("time", text="Time")
        
        self.trans_tree.column("action", width=80, anchor="center")
        self.trans_tree.column("product", width=120)
        self.trans_tree.column("time", width=100, anchor="center")
        
        self.trans_tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.trans_tree.yview)
        
        # Load recent transactions
        with open("transactions.json", "r") as f:
            transactions = json.load(f)
        
        for transaction in transactions[-10:][::-1]:  # Show last 10, newest first
            self.trans_tree.insert("", "end", values=(
                transaction["action"],
                transaction["product_name"],
                datetime.strptime(transaction["timestamp"], "%Y-%m-%d %H:%M:%S").strftime("%m/%d %H:%M")
            ))

    def view_products(self):
        self.clear_window()
        self.setup_navigation("Products")
        
        # Content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Search and filter section
        filter_frame = ttk.Frame(content_frame)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Search:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(filter_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        
        ttk.Button(filter_frame, text="Search", style="Secondary.TButton", 
                  command=self.search_products).pack(side="left", padx=5)
        
        ttk.Button(filter_frame, text="Clear", command=self.clear_search).pack(side="left", padx=5)
        
        # Category filter
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        categories = sorted(set(p["category"] for p in inventory))
        ttk.Label(filter_frame, text="Category:").pack(side="left", padx=(20,5))
        
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(filter_frame, textvariable=self.category_var, 
                                         values=categories, state="readonly")
        self.category_menu.pack(side="left", padx=5)
        
        ttk.Button(filter_frame, text="Filter", style="Secondary.TButton", 
                  command=self.filter_by_category).pack(side="left", padx=5)
        


        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(btn_frame, text="Add Product", style="Secondary.TButton", 
                  command=self.add_product).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Edit Selected", style="Primary.TButton", 
                  command=self.edit_selected_product).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Delete Selected", style="Danger.TButton", 
                  command=self.delete_selected_product).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Add Stock", style="Secondary.TButton", 
                  command=self.add_stock).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Remove Stock", style="Danger.TButton", 
                  command=self.remove_stock).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Refresh", command=self.load_products).pack(side="right", padx=5)


        
        # Products table
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("id", "name", "category", "price", "quantity", "status", "last_updated")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                                yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("category", text="Category")
        self.tree.heading("price", text="Price")
        self.tree.heading("quantity", text="Qty")
        self.tree.heading("status", text="Status")
        self.tree.heading("last_updated", text="Last Updated")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("category", width=120)
        self.tree.column("price", width=80, anchor="e")
        self.tree.column("quantity", width=60, anchor="center")
        self.tree.column("status", width=120, anchor="center")
        self.tree.column("last_updated", width=140)
        
        self.tree.pack(fill="both", expand=True)
        
        # Action buttons
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(btn_frame, text="Add Product", style="Secondary.TButton", 
                  command=self.add_product).pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="Edit Selected", style="Primary.TButton", 
                  command=self.edit_selected_product).pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="Delete Selected", style="Danger.TButton", 
                  command=self.delete_selected_product).pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="Refresh", command=self.load_products).pack(side="right", padx=5)
        
        # Load products
        self.load_products()
        
        # Bind double click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_selected_product())

    def load_products(self):
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        self.tree.delete(*self.tree.get_children())
        
        for product in inventory:
            status = "In Stock"
            if product["quantity"] <= 0:
                status = "Out of Stock"
            elif product["quantity"] <= product["min_stock"]:
                status = "Low Stock"
            
            self.tree.insert("", "end", values=(
                product["id"],
                product["name"],
                product["category"],
                f"${product['price']:,.2f}" if product['price'] >= 1 else f"${product['price']:.2f}",
                product["quantity"],
                status,
                datetime.strptime(product["last_updated"], "%Y-%m-%d %H:%M:%S").strftime("%m/%d/%Y %H:%M")
            ), tags=(status.lower().replace(" ", ""),))
        
        # Configure tag colors
        self.tree.tag_configure("instock", background="#e8f5e9")
        self.tree.tag_configure("lowstock", background="#fff8e1")
        self.tree.tag_configure("outofstock", background="#ffebee")

    def search_products(self):
        query = self.search_entry.get().lower()
        
        for item in self.tree.get_children():
            values = [str(v).lower() for v in self.tree.item(item, "values")]
            if any(query in v for v in values):
                self.tree.selection_add(item)
                self.tree.focus(item)
                return
        
        messagebox.showinfo("Search", "No matching products found", parent=self.root)

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.category_var.set("")
        self.load_products()

    def filter_by_category(self):
        category = self.category_var.get()
        if not category:
            return
        
        for item in self.tree.get_children():
            if self.tree.item(item, "values")[2] == category:
                self.tree.selection_add(item)
            else:
                self.tree.selection_remove(item)

    def add_product(self):
        self.clear_window()
        self.setup_navigation("Add Product")
        
        # Form frame
        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Add New Product", font=('Helvetica', 16, 'bold')).grid(
            row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Form fields
        fields = [
            ("name", "Product Name:", "entry"),
            ("category", "Category:", "entry"),
            ("price", "Unit Price ($):", "spin"),
            ("quantity", "Quantity:", "spin"),
            ("min_stock", "Minimum Stock Level:", "spin"),
            ("description", "Description:", "text")
        ]
        
        self.entries = {}
        for i, (field, label, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i+1, column=0, sticky="e", padx=5, pady=5)
            
            if widget_type == "entry":
                entry = ttk.Entry(form_frame, font=('Helvetica', 11))
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
                form_frame.columnconfigure(1, weight=1)
            elif widget_type == "spin":
                entry = ttk.Spinbox(form_frame, from_=0, to=100000, increment=1)
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
            elif widget_type == "text":
                entry = tk.Text(form_frame, height=4, width=30, font=('Helvetica', 11))
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
            
            self.entries[field] = entry
        
        # Initialize spinboxes with default values
        self.entries["price"].configure(from_=0, to=10000, increment=0.01, format="%.2f")
        self.entries["price"].set(0.00)
        self.entries["quantity"].set(0)
        self.entries["min_stock"].set(0)
        
        # Button frame
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Save Product", style="Secondary.TButton", 
                  command=self.save_product).pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="Cancel", command=self.view_products).pack(side="left", padx=5)

    def save_product(self):
        try:
            # Validate inputs
            name = self.entries["name"].get().strip()
            if not name:
                raise ValueError("Product name is required")
            
            category = self.entries["category"].get().strip()
            if not category:
                raise ValueError("Category is required")
            
            price = float(self.entries["price"].get())
            if price <= 0:
                raise ValueError("Price must be positive")
            
            quantity = int(self.entries["quantity"].get())
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
            
            min_stock = int(self.entries["min_stock"].get())
            if min_stock < 0:
                raise ValueError("Minimum stock cannot be negative")
            
            description = self.entries["description"].get("1.0", tk.END).strip()
            
            # Get existing inventory
            with open("inventory.json", "r") as f:
                inventory = json.load(f)
            
            # Generate new ID
            new_id = max((p["id"] for p in inventory), default=0) + 1
            
            # Add new product
            new_product = {
                "id": new_id,
                "name": name,
                "category": category,
                "price": price,
                "quantity": quantity,
                "min_stock": min_stock,
                "description": description,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            inventory.append(new_product)
            
            # Save back to file
            with open("inventory.json", "w") as f:
                json.dump(inventory, f, indent=2)
            
            # Record transaction
            self.record_transaction("ADD", new_product)
            
            messagebox.showinfo("Success", "Product added successfully!", parent=self.root)
            self.view_products()
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e), parent=self.root)

    def edit_selected_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a product to edit", parent=self.root)
            return
        
        item = self.tree.item(selected[0])
        product_id = item["values"][0]
        
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        product = next((p for p in inventory if p["id"] == product_id), None)
        if not product:
            messagebox.showerror("Error", "Product not found", parent=self.root)
            return
        
        self.clear_window()
        self.setup_navigation("Edit Product")
        
        # Form frame
        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ttk.Label(form_frame, text="Edit Product", font=('Helvetica', 16, 'bold'),
                 foreground=self.colors["primary"]).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Form fields
        fields = [
            ("name", "Product Name:", "entry"),
            ("category", "Category:", "entry"),
            ("price", "Unit Price ($):", "spin"),
            ("quantity", "Quantity:", "spin"),
            ("min_stock", "Minimum Stock Level:", "spin"),
            ("description", "Description:", "text")
        ]
        
        self.entries = {}
        for i, (field, label, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i+1, column=0, sticky="e", padx=5, pady=5)
            
            if widget_type == "entry":
                entry = ttk.Entry(form_frame, font=('Helvetica', 11))
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
                form_frame.columnconfigure(1, weight=1)
            elif widget_type == "spin":
                entry = ttk.Spinbox(form_frame, from_=0, to=100000, increment=1)
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
            elif widget_type == "text":
                entry = tk.Text(form_frame, height=4, width=30, font=('Helvetica', 11))
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
            
            self.entries[field] = entry
        
        # Initialize spinboxes
        self.entries["price"].configure(from_=0, to=10000, increment=0.01, format="%.2f")
        
        # Pre-fill fields with existing data
        self.entries["name"].insert(0, product["name"])
        self.entries["category"].insert(0, product["category"])
        self.entries["price"].set(str(product["price"]))
        self.entries["quantity"].set(str(product["quantity"]))
        self.entries["min_stock"].set(str(product["min_stock"]))
        self.entries["description"].insert("1.0", product.get("description", ""))
        
        # Hidden ID field
        self.editing_id = product["id"]
        
        # Button frame
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Update Product", style="Secondary.TButton", 
                  command=self.update_product).pack(side="left", padx=5)
        
        ttk.Button(btn_frame, text="Cancel", command=self.view_products).pack(side="left", padx=5)

    def update_product(self):
        try:
            # Validate inputs
            name = self.entries["name"].get().strip()
            if not name:
                raise ValueError("Product name is required")
            
            category = self.entries["category"].get().strip()
            if not category:
                raise ValueError("Category is required")
            
            price = float(self.entries["price"].get())
            if price <= 0:
                raise ValueError("Price must be positive")
            
            quantity = int(self.entries["quantity"].get())
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
            
            min_stock = int(self.entries["min_stock"].get())
            if min_stock < 0:
                raise ValueError("Minimum stock cannot be negative")
            
            description = self.entries["description"].get("1.0", tk.END).strip()
            
            # Get existing inventory
            with open("inventory.json", "r") as f:
                inventory = json.load(f)
            
            # Find and update product
            updated = False
            old_product = None
            new_product = None
            
            for i, product in enumerate(inventory):
                if product["id"] == self.editing_id:
                    old_product = product.copy()
                    
                    inventory[i] = {
                        "id": self.editing_id,
                        "name": name,
                        "category": category,
                        "price": price,
                        "quantity": quantity,
                        "min_stock": min_stock,
                        "description": description,
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    new_product = inventory[i]
                    updated = True
                    break
            
            if not updated:
                raise ValueError("Product not found")
            
            # Save back to file
            with open("inventory.json", "w") as f:
                json.dump(inventory, f, indent=2)
            
            # Record transaction
            self.record_transaction("UPDATE", new_product, old_product)
            
            messagebox.showinfo("Success", "Product updated successfully!", parent=self.root)
            self.view_products()
        
        except ValueError as e:
            messagebox.showerror("Input Error", str(e), parent=self.root)

    def delete_selected_product(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a product to delete", parent=self.root)
            return
        
        item = self.tree.item(selected[0])
        product_id = item["values"][0]
        
        if not messagebox.askyesno("Confirm Delete", 
                                  "Are you sure you want to delete this product?\nThis action cannot be undone.", 
                                  parent=self.root):
            return
        
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        # Find and remove product
        deleted_product = None
        new_inventory = []
        
        for product in inventory:
            if product["id"] == product_id:
                deleted_product = product
            else:
                new_inventory.append(product)
        
        if not deleted_product:
            messagebox.showerror("Error", "Product not found", parent=self.root)
            return
        
        # Save back to file
        with open("inventory.json", "w") as f:
            json.dump(new_inventory, f, indent=2)
        
        # Record transaction
        self.record_transaction("DELETE", deleted_product)
        
        messagebox.showinfo("Success", "Product deleted successfully!", parent=self.root)
        self.view_products()


    def add_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a product to add stock", parent=self.root)
            return

        item = self.tree.item(selected[0])
        product_id = item["values"][0]

        with open("inventory.json", "r") as f:
            inventory = json.load(f)

        product = next((p for p in inventory if p["id"] == product_id), None)
        if not product:
            messagebox.showerror("Error", "Product not found", parent=self.root)
            return

        self.clear_window()
        self.setup_navigation("Add Stock")

        # Form frame
        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(form_frame, text="Add Stock", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Form fields
        fields = [
            ("quantity", "Quantity to Add:", "spin"),
        ]

        self.entries = {}
        for i, (field, label, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i+1, column=0, sticky="e", padx=5, pady=5)

            if widget_type == "spin":
                entry = ttk.Spinbox(form_frame, from_=0, to=100000, increment=1)
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
            elif widget_type == "text":
                entry = tk.Text(form_frame, height=4, width=30, font=('Helvetica', 11))
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)

            self.entries[field] = entry

        # Initialize spinboxes
        self.entries["quantity"].set(0)

        # Hidden ID field
        self.adding_stock_id = product_id

        # Button frame
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(btn_frame, text="Add Stock", style="Secondary.TButton", 
                  command=self.save_stock_addition).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Cancel", command=self.view_products).pack(side="left", padx=5)

    def save_stock_addition(self):
        try:
            # Validate inputs
            quantity = int(self.entries["quantity"].get())
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")

            # Get existing inventory
            with open("inventory.json", "r") as f:
                inventory = json.load(f)

            # Find and update product
            updated = False
            for i, product in enumerate(inventory):
                if product["id"] == self.adding_stock_id:
                    inventory[i]["quantity"] += quantity
                    inventory[i]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    updated = True
                    break

            if not updated:
                raise ValueError("Product not found")

            # Save back to file
            with open("inventory.json", "w") as f:
                json.dump(inventory, f, indent=2)

            # Record transaction
            self.record_transaction("STOCK_ADD", {"id": self.adding_stock_id, "quantity": quantity})

            messagebox.showinfo("Success", "Stock added successfully!", parent=self.root)
            self.view_products()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e), parent=self.root)

    def remove_stock(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a product to remove stock", parent=self.root)
            return

        item = self.tree.item(selected[0])
        product_id = item["values"][0]

        with open("inventory.json", "r") as f:
            inventory = json.load(f)

        product = next((p for p in inventory if p["id"] == product_id), None)
        if not product:
            messagebox.showerror("Error", "Product not found", parent=self.root)
            return

        self.clear_window()
        self.setup_navigation("Remove Stock")

        # Form frame
        form_frame = ttk.Frame(self.root, padding=20)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(form_frame, text="Remove Stock", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Form fields
        fields = [
            ("quantity", "Quantity to Remove:", "spin"),
        ]

        self.entries = {}
        for i, (field, label, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i+1, column=0, sticky="e", padx=5, pady=5)

            if widget_type == "spin":
                entry = ttk.Spinbox(form_frame, from_=0, to=100000, increment=1)
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
            elif widget_type == "text":
                entry = tk.Text(form_frame, height=4, width=30, font=('Helvetica', 11))
                entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)

            self.entries[field] = entry

        # Initialize spinboxes
        self.entries["quantity"].set(0)

        # Hidden ID field
        self.removing_stock_id = product_id

        # Button frame
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(btn_frame, text="Remove Stock", style="Danger.TButton", 
                  command=self.save_stock_removal).pack(side="left", padx=5)

        ttk.Button(btn_frame, text="Cancel", command=self.view_products).pack(side="left", padx=5)

    def save_stock_removal(self):
        try:
            # Validate inputs
            quantity = int(self.entries["quantity"].get())
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")

            # Get existing inventory
            with open("inventory.json", "r") as f:
                inventory = json.load(f)

            # Find and update product
            updated = False
            for i, product in enumerate(inventory):
                if product["id"] == self.removing_stock_id:
                    if product["quantity"] < quantity:
                        raise ValueError("Not enough stock to remove")
                    inventory[i]["quantity"] -= quantity
                    inventory[i]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    updated = True
                    break

            if not updated:
                raise ValueError("Product not found")

            # Save back to file
            with open("inventory.json", "w") as f:
                json.dump(inventory, f, indent=2)

            # Record transaction
            self.record_transaction("STOCK_REMOVE", {"id": self.removing_stock_id, "quantity": quantity})

            messagebox.showinfo("Success", "Stock removed successfully!", parent=self.root)
            self.view_products()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e), parent=self.root)



    def reports_dashboard(self):
        self.clear_window()
        self.setup_navigation("Reports")
        
        # Content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Reports buttons
        reports_frame = ttk.Frame(content_frame)
        reports_frame.pack(fill="both", expand=True)
        
        reports = [
            ("Inventory Summary", self.inventory_summary_report, "pie-chart"),
            ("Low Stock Alerts", self.low_stock_report, "alert"),
            ("Category Analysis", self.category_analysis_report, "bar-chart"),
            ("Value Distribution", self.value_distribution_report, "dollar")
        ]
        
        for i, (title, command, icon) in enumerate(reports):
            card = ttk.Frame(reports_frame, relief="groove", borderwidth=2, padding=10)
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            card.columnconfigure(0, weight=1)
            
            # Placeholder for icon
            ttk.Label(card, text=f"[{icon}]", font=('Helvetica', 24), 
                     foreground=self.colors["primary"]).pack(pady=(0, 10))
            
            ttk.Label(card, text=title, font=('Helvetica', 12, 'bold')).pack()
            
            ttk.Button(card, text="View Report", style="Primary.TButton", 
                      command=command).pack(fill="x", pady=(10, 0))

    def inventory_summary_report(self):
        self.clear_window()
        self.setup_navigation("Inventory Summary")
        
        # Content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load inventory data
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        # Calculate summary
        total_value = sum(p["price"]*p["quantity"] for p in inventory)
        low_stock = sum(1 for p in inventory if p["quantity"] <= p["min_stock"])
        out_of_stock = sum(1 for p in inventory if p["quantity"] <= 0)
        
        # Chart frame
        chart_frame = ttk.Frame(content_frame)
        chart_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        fig = plt.figure(figsize=(10, 6), dpi=80)
        ax = fig.add_subplot(111)
        
        categories = {}
        for product in inventory:
            if product['category'] not in categories:
                categories[product['category']] = 0
            categories[product['category']] += product['price'] * product['quantity']
        
        labels = list(categories.keys())
        values = list(categories.values())
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90, 
            colors=plt.cm.Pastel1(np.linspace(0, 1, len(labels))),
            textprops={'fontsize': 10}
        )
        
        ax.set_title('Inventory Value by Category', fontsize=14, fontweight='bold')
        ax.axis('equal')
        
        chart = FigureCanvasTkAgg(fig, chart_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)
        
        # Summary frame
        summary_frame = ttk.Frame(content_frame)
        summary_frame.pack(fill="x", pady=(10, 0))
        
        stats_data = [
            {"title": "Total Products", "value": len(inventory), "color": "#4e79a7"},
            {"title": "Inventory Value", "value": f"${total_value:,.2f}", "color": "#f28e2b"},
            {"title": "Low Stock Items", "value": low_stock, "color": "#e15759"},
            {"title": "Out of Stock Items", "value": out_of_stock, "color": "#76b7b2"}
        ]
        
        for i, stat in enumerate(stats_data):
            card = ttk.Frame(summary_frame, relief="groove", borderwidth=2, padding=10)
            card.grid(row=0, column=i, padx=5, sticky="nsew")
            summary_frame.columnconfigure(i, weight=1)
            
            ttk.Label(card, text=stat["title"], font=('Helvetica', 10, 'bold'), 
                     foreground=stat["color"]).pack(anchor="w")
            ttk.Label(card, text=str(stat["value"]), font=('Helvetica', 16, 'bold')).pack()

    def low_stock_report(self):
        self.clear_window()
        self.setup_navigation("Low Stock Report")
        
        # Content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load inventory data
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        low_stock_items = [p for p in inventory if p["quantity"] <= p["min_stock"]]
        
        if not low_stock_items:
            ttk.Label(content_frame, text="No low stock items found!", font=('Helvetica', 14)).pack(pady=50)
            return
        
        # Chart frame
        chart_frame = ttk.Frame(content_frame)
        chart_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        fig = plt.figure(figsize=(10, 6), dpi=80)
        ax = fig.add_subplot(111)
        
        # Sort by percentage of stock remaining
        low_stock_items.sort(key=lambda x: (x["quantity"] / x["min_stock"]) if x["min_stock"] > 0 else 0)
        
        product_names = [p["name"] for p in low_stock_items]
        quantities = [p["quantity"] for p in low_stock_items]
        min_stocks = [p["min_stock"] for p in low_stock_items]
        
        x = range(len(product_names))
        width = 0.35
        
        bars1 = ax.bar(x, quantities, width, label='Current Stock', color='#f28e2b')
        bars2 = ax.bar([i + width for i in x], min_stocks, width, label='Minimum Stock', color='#e15759')
        
        ax.set_xlabel('Products', fontsize=12)
        ax.set_ylabel('Quantity', fontsize=12)
        ax.set_title('Low Stock Items Report', fontsize=14, fontweight='bold')
        ax.set_xticks([i + width / 2 for i in x])
        ax.set_xticklabels(product_names, rotation=45, ha='right', fontsize=10)
        ax.legend(fontsize=10)
        
        fig.tight_layout()
        chart = FigureCanvasTkAgg(fig, chart_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)
        
        # Table frame
        table_frame = ttk.Frame(content_frame)
        table_frame.pack(fill="both", expand=True, pady=(20, 0))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("name", "category", "quantity", "min_stock", "needed")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", 
                           yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)
        
        tree.heading("name", text="Product Name")
        tree.heading("category", text="Category")
        tree.heading("quantity", text="Current Stock")
        tree.heading("min_stock", text="Minimum Stock")
        tree.heading("needed", text="To Order")
        
        tree.column("name", width=200)
        tree.column("category", width=150)
        tree.column("quantity", width=100, anchor="center")
        tree.column("min_stock", width=100, anchor="center")
        tree.column("needed", width=100, anchor="center")
        
        tree.pack(fill="both", expand=True)
        
        for product in low_stock_items:
            needed = max(product["min_stock"] - product["quantity"], 0)
            
            tree.insert("", "end", values=(
                product["name"],
                product["category"],
                product["quantity"],
                product["min_stock"],
                needed if needed > 0 else "✔"
            ))

    def category_analysis_report(self):
        self.clear_window()
        self.setup_navigation("Category Analysis")
        
        # Content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load inventory data
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        # Chart frame
        chart_frame = ttk.Frame(content_frame)
        chart_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        fig = plt.figure(figsize=(10, 6), dpi=80)
        ax = fig.add_subplot(111)
        
        # Group data by category
        categories = {}
        for product in inventory:
            if product["category"] not in categories:
                categories[product["category"]] = {
                    "count": 0,
                    "total_value": 0,
                    "items": []
                }
            categories[product["category"]]["count"] += 1
            categories[product["category"]]["total_value"] += product["price"] * product["quantity"]
            categories[product["category"]]["items"].append(product)
        
        # Sort categories by count
        sorted_categories = sorted(categories.items(), key=lambda x: x[1]["count"], reverse=True)
        category_names = [c[0] for c in sorted_categories]
        counts = [c[1]["count"] for c in sorted_categories]
        values = [c[1]["total_value"] for c in sorted_categories]
        
        # Create dual-axis chart
        ax1 = ax
        ax1.bar(category_names, counts, color='#4e79a7', alpha=0.7, label='Product Count')
        ax1.set_xlabel('Categories', fontsize=12)
        ax1.set_ylabel('Number of Products', color='#4e79a7', fontsize=12)
        ax1.tick_params(axis='y', labelcolor='#4e79a7')
        
        ax2 = ax1.twinx()
        ax2.plot(category_names, values, color='#e15759', marker='o', label='Total Value ($)')
        ax2.set_ylabel('Total Inventory Value ($)', color='#e15759', fontsize=12)
        ax2.tick_params(axis='y', labelcolor='#e15759')
        
        ax.set_title('Category Analysis: Product Count vs. Inventory Value', 
                    fontsize=14, fontweight='bold')
        
        # Combine legends from both axes
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc='upper right')
        
        plt.xticks(rotation=45, ha='right')
        fig.tight_layout()
        
        chart = FigureCanvasTkAgg(fig, chart_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)

    def value_distribution_report(self):
        self.clear_window()
        self.setup_navigation("Value Distribution")
        
        # Content frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load inventory data
        with open("inventory.json", "r") as f:
            inventory = json.load(f)
        
        # Chart frame
        chart_frame = ttk.Frame(content_frame)
        chart_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        fig = plt.figure(figsize=(10, 6), dpi=80)
        ax = fig.add_subplot(111)
        
        # Prepare data
        values = [p["price"] * p["quantity"] for p in inventory]
        names = [p["name"] for p in inventory]
        
        # Sort by value
        sorted_values = sorted(zip(values, names), reverse=True)
        values = [v[0] for v in sorted_values]
        names = [v[1] for v in sorted_values]
        
        # Create waterfall chart
        pos = range(len(values))
        ax.bar(pos, values, color='#76b7b2', edgecolor='black')
        
        ax.set_xlabel('Products', fontsize=12)
        ax.set_ylabel('Inventory Value ($)', fontsize=12)
        ax.set_title('Product Value Distribution', fontsize=14, fontweight='bold')
        
        ax.set_xticks(pos)
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        
        # Add value labels
        for i, v in enumerate(values):
            if v > 0:
                ax.text(i, v, f"${v:,.0f}", ha='center', va='bottom', fontsize=8)
        
        fig.tight_layout()
        chart = FigureCanvasTkAgg(fig, chart_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill="both", expand=True)
        
        # Summary frame
        summary_frame = ttk.Frame(content_frame)
        summary_frame.pack(fill="x", pady=(10, 0))
        
        stats_data = [
            {"title": "Total Inventory Value", "value": f"${sum(values):,.2f}", "color": "#76b7b2"},
            {"title": "Most Valuable Item", 
             "value": f"{names[0]} (${values[0]:,.2f})", 
             "color": "#4e79a7"},
            {"title": "Number of Products", "value": len(values), "color": "#f28e2b"}
        ]
        
        for i, stat in enumerate(stats_data):
            card = ttk.Frame(summary_frame, relief="groove", borderwidth=2, padding=10)
            card.grid(row=0, column=i, padx=5, sticky="nsew")
            summary_frame.columnconfigure(i, weight=1)
            
            ttk.Label(card, text=stat["title"], font=('Helvetica', 10, 'bold'), 
                     foreground=stat["color"]).pack(anchor="w")
            ttk.Label(card, text=str(stat["value"]), font=('Helvetica', 12)).pack()

    def record_transaction(self, action, product, old_product=None):
        with open("transactions.json", "r") as f:
            transactions = json.load(f)
        
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": self.current_user,
            "action": action,
            "product_id": product["id"],
            "product_name": product["name"],
            "details": {
                "new": product,
                "old": old_product
            }
        }
        
        transactions.append(transaction)
        
        with open("transactions.json", "w") as f:
            json.dump(transactions, f, indent=2)

    def logout(self):
        self.current_user = None
        self.login_screen()

    def setup_navigation(self, current_screen):
        # Header frame
        header_frame = ttk.Frame(self.root, padding=10)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Screen title
        ttk.Label(header_frame, text=current_screen, font=('Helvetica', 18, 'bold')).pack(side="left")
        
        # Back button
        ttk.Button(header_frame, text="Back to Main Menu", style="Primary.TButton", 
                  command=self.main_dashboard).pack(side="right")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()

