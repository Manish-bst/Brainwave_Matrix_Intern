import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os
from tkinter import simpledialog
import csv

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("1200x750")
        self.root.resizable(False, False)
        
        # Initialize data files
        self.data_dir = "inventory_data"
        self.products_file = os.path.join(self.data_dir, "products.json")
        self.users_file = os.path.join(self.data_dir, "users.json")
        self.transactions_file = os.path.join(self.data_dir, "transactions.json")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # Initialize empty data structures if files don't exist
        self.products = self.load_data(self.products_file)
        self.users = self.load_data(self.users_file)
        self.transactions = self.load_data(self.transactions_file)
        
        # Add default admin user if no users exist
        if not self.users:
            self.users = {"admin": {"password": "admin123", "role": "admin"}}
            self.save_data(self.users_file, self.users)
        
        # Current user session
        self.current_user = None
        
        # Theme colors
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#e74c3c"
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Show login screen
        self.show_login()

    def load_data(self, file_path):
        """Load JSON data from file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    return data if data else {}
            return {}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            return {}

    def save_data(self, file_path, data):
        """Save data to JSON file"""
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False

    def login(self, username, password):
        """Handle user login"""
        if username in self.users and self.users[username]["password"] == password:
            self.current_user = username
            self.show_main_app()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_login(self):
        """Display login screen"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main login frame
        login_frame = tk.Frame(self.root, bg=self.bg_color)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        login_title = tk.Label(
            login_frame, 
            text="Inventory Management System", 
            font=("Helvetica", 18, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        login_title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        # Username label and entry
        username_label = tk.Label(
            login_frame, 
            text="Username:", 
            font=("Helvetica", 12),
            bg=self.bg_color
        )
        username_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.username_entry = tk.Entry(
            login_frame, 
            font=("Helvetica", 12),
            width=25
        )
        self.username_entry.grid(row=1, column=1, pady=5)
        
        # Password label and entry
        password_label = tk.Label(
            login_frame, 
            text="Password:", 
            font=("Helvetica", 12),
            bg=self.bg_color
        )
        password_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        
        self.password_entry = tk.Entry(
            login_frame, 
            font=("Helvetica", 12),
            show="*", 
            width=25
        )
        self.password_entry.grid(row=2, column=1, pady=5)
        
        # Login button
        login_button = tk.Button(
            login_frame, 
            text="Login", 
            font=("Helvetica", 12, "bold"),
            bg=self.secondary_color,
            fg="white",
            width=20,
            command=lambda: self.login(
                self.username_entry.get(),
                self.password_entry.get()
            )
        )
        login_button.grid(row=3, column=0, columnspan=2, pady=(15, 5))
        
        # Default credentials for testing
        default_label = tk.Label(
            login_frame,
            text="(Default: admin/admin123)",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg="#666666"
        )
        default_label.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: login_button.invoke())

    def show_main_app(self):
        """Display main application after successful login"""
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main container frame
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header frame
        header_frame = tk.Frame(main_frame, bg=self.primary_color)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title label
        title_label = tk.Label(
            header_frame, 
            text=f"Inventory Management System - Welcome, {self.current_user}",
            font=("Helvetica", 14, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        title_label.pack(side="left", padx=10, pady=10)
        
        # Logout button
        logout_button = tk.Button(
            header_frame, 
            text="Logout", 
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=self.show_login
        )
        logout_button.pack(side="right", padx=10, pady=10)
        
        # Navigation frame
        nav_frame = tk.Frame(main_frame, bg=self.bg_color)
        nav_frame.pack(fill="x", pady=(0, 10))
        
        # Navigation buttons
        products_button = tk.Button(
            nav_frame,
            text="Products",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            width=15,
            command=self.show_products_tab
        )
        products_button.pack(side="left", padx=5)
        
        inventory_button = tk.Button(
            nav_frame,
            text="Inventory",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            width=15,
            command=self.show_inventory_tab
        )
        inventory_button.pack(side="left", padx=5)
        
        reports_button = tk.Button(
            nav_frame,
            text="Reports",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            width=15,
            command=self.show_reports_tab
        )
        reports_button.pack(side="left", padx=5)
        
        users_button = tk.Button(
            nav_frame,
            text="User Management",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            width=15,
            command=self.show_users_tab,
            state="normal" if self.users[self.current_user]["role"] == "admin" else "disabled"
        )
        users_button.pack(side="left", padx=5)
        
        # Tab content frame
        self.tab_content_frame = tk.Frame(main_frame, bg=self.bg_color)
        self.tab_content_frame.pack(fill="both", expand=True)
        
        # Show products tab by default
        self.show_products_tab()

    def show_products_tab(self):
        """Display products management tab"""
        # Clear tab content
        for widget in self.tab_content_frame.winfo_children():
            widget.destroy()
        
        # Products tab frame
        products_frame = tk.Frame(self.tab_content_frame, bg=self.bg_color)
        products_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Products header
        products_header = tk.Frame(products_frame, bg=self.bg_color)
        products_header.pack(fill="x", pady=(0, 10))
        
        products_label = tk.Label(
            products_header, 
            text="Product Management", 
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color
        )
        products_label.pack(side="left")
        
        add_button = tk.Button(
            products_header, 
            text="Add Product", 
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.add_product_dialog
        )
        add_button.pack(side="right", padx=5)
        
        # Search frame
        search_frame = tk.Frame(products_frame, bg=self.bg_color)
        search_frame.pack(fill="x", pady=(0, 10))
        
        search_label = tk.Label(
            search_frame,
            text="Search:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        search_label.pack(side="left", padx=5)
        
        self.search_entry = tk.Entry(
            search_frame,
            font=("Helvetica", 10),
            width=40
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_products)
        
        search_button = tk.Button(
            search_frame,
            text="Search",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=lambda: self.search_products(None)
        )
        search_button.pack(side="left", padx=5)
        
        # Products treeview
        self.products_tree = ttk.Treeview(
            products_frame,
            columns=("id", "name", "category", "price", "quantity", "threshold"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.products_tree.heading("id", text="ID", anchor="w")
        self.products_tree.heading("name", text="Name", anchor="w")
        self.products_tree.heading("category", text="Category", anchor="w")
        self.products_tree.heading("price", text="Price ($)", anchor="w")
        self.products_tree.heading("quantity", text="Quantity", anchor="w")
        self.products_tree.heading("threshold", text="Low Stock Threshold", anchor="w")
        
        self.products_tree.column("id", width=80)
        self.products_tree.column("name", width=200)
        self.products_tree.column("category", width=150)
        self.products_tree.column("price", width=100)
        self.products_tree.column("quantity", width=100)
        self.products_tree.column("threshold", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(products_frame, orient="vertical", command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.products_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Action buttons frame
        action_frame = tk.Frame(products_frame, bg=self.bg_color)
        action_frame.pack(fill="x", pady=(10, 0))
        
        edit_button = tk.Button(
            action_frame,
            text="Edit Selected",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.edit_product_dialog
        )
        edit_button.pack(side="left", padx=5)
        
        delete_button = tk.Button(
            action_frame,
            text="Delete Selected",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=self.delete_product
        )
        delete_button.pack(side="left", padx=5)
        
        refresh_button = tk.Button(
            action_frame,
            text="Refresh",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.refresh_products_list
        )
        refresh_button.pack(side="right", padx=5)
        
        # Populate products tree
        self.refresh_products_list()

    def refresh_products_list(self):
        """Refresh the products treeview with current data"""
        self.products_tree.delete(*self.products_tree.get_children())
        for product_id, product_data in self.products.items():
            self.products_tree.insert(
                "", 
                "end", 
                values=(
                    product_id,
                    product_data["name"],
                    product_data["category"],
                    f"${product_data['price']:.2f}",
                    product_data["quantity"],
                    product_data["threshold"]
                )
            )
        
        # Highlight low-stock items
        self.highlight_low_stock()

    def highlight_low_stock(self):
        """Highlight items with quantity below threshold"""
        for item in self.products_tree.get_children():
            values = self.products_tree.item(item)['values']
            quantity = int(values[4])
            threshold = int(values[5])
            
            if quantity <= threshold:
                self.products_tree.tag_configure('low_stock', background='#ffcccc')
                self.products_tree.item(item, tags=('low_stock',))

    def search_products(self, event):
        """Search products by name or ID"""
        search_term = self.search_entry.get().lower()
        
        if not search_term:
            self.refresh_products_list()
            return
            
        for item in self.products_tree.get_children():
            values = self.products_tree.item(item)['values']
            item_text = f"{values[0]} {values[1]} {values[2]}".lower()
            
            if search_term in item_text:
                self.products_tree.item(item, tags=())
            else:
                self.products_tree.detach(item)

    def add_product_dialog(self):
        """Show dialog for adding new product"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("400x400")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Form fields
        fields = [
            ("Name:", "entry", ""),
            ("Category:", "entry", ""),
            ("Description:", "text", ""),
            ("Price ($):", "entry", ""),
            ("Quantity:", "entry", ""),
            ("Low Stock Threshold:", "entry", ""),
            ("Supplier:", "entry", "")
        ]
        
        self.add_product_vars = {}
        
        for i, (label_text, field_type, default_value) in enumerate(fields):
            label = tk.Label(
                form_frame, 
                text=label_text, 
                font=("Helvetica", 10),
                bg=self.bg_color
            )
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            
            if field_type == "entry":
                var = tk.StringVar(value=default_value)
                entry = tk.Entry(
                    form_frame,
                    font=("Helvetica", 10),
                    textvariable=var,
                    width=30
                )
                entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
                self.add_product_vars[label_text] = var
            elif field_type == "text":
                text = tk.Text(
                    form_frame,
                    font=("Helvetica", 10),
                    width=30,
                    height=5,
                    wrap="word"
                )
                text.grid(row=i, column=1, sticky="w", padx=5, pady=5)
                self.add_product_vars[label_text] = text
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.bg_color)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(20, 0))
        
        add_button = tk.Button(
            button_frame,
            text="Add Product",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=lambda: self.add_product(dialog)
        )
        add_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=10)
        
    def add_product(self, dialog):
        """Add new product to inventory"""
        try:
            # Validate inputs
            name = self.add_product_vars["Name:"].get().strip()
            category = self.add_product_vars["Category:"].get().strip()
            description = self.add_product_vars["Description:"].get("1.0", tk.END).strip()
            price_str = self.add_product_vars["Price ($):"].get().strip()
            quantity_str = self.add_product_vars["Quantity:"].get().strip()
            threshold_str = self.add_product_vars["Low Stock Threshold:"].get().strip()
            supplier = self.add_product_vars["Supplier:"].get().strip()
            
            if not all([name, category, price_str, quantity_str, threshold_str]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            try:
                price = float(price_str)
                quantity = int(quantity_str)
                threshold = int(threshold_str)
                
                if price <= 0 or quantity < 0 or threshold < 0:
                    raise ValueError
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price, quantity, and threshold")
                return
            
            # Generate product ID
            product_id = f"P{len(self.products) + 1:04d}"
            
            # Add product to inventory
            self.products[product_id] = {
                "name": name,
                "category": category,
                "description": description,
                "price": price,
                "quantity": quantity,
                "threshold": threshold,
                "supplier": supplier,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "modified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Record transaction
            self.record_transaction(
                product_id,
                "add",
                quantity,
                f"Product {name} added to inventory"
            )
            
            # Save data
            self.save_data(self.products_file, self.products)
            
            # Refresh products list
            self.refresh_products_list()
            # Close dialog
            dialog.destroy()
            
            messagebox.showinfo("Success", f"Product {name} added successfully with ID {product_id}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")

    def edit_product_dialog(self):
        """Show dialog for editing selected product"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to edit")
            return
            
        item = selected[0]
        product_id = self.products_tree.item(item)["values"][0]
        product = self.products[product_id]
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Product {product_id}")
        dialog.geometry("400x450")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product ID label (not editable)
        id_label = tk.Label(
            form_frame, 
            text=f"Product ID: {product_id}",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        id_label.grid(row=0, columnspan=2, pady=(0, 10))
        
        # Form fields
        fields = [
            ("Name:", "entry", product["name"]),
            ("Category:", "entry", product["category"]),
            ("Description:", "text", product["description"]),
            ("Price ($):", "entry", product["price"]),
            ("Quantity:", "entry", product["quantity"]),
            ("Low Stock Threshold:", "entry", product["threshold"]),
            ("Supplier:", "entry", product["supplier"])
        ]
        
        self.edit_product_vars = {}
        
        for i, (label_text, field_type, default_value) in enumerate(fields):
            label = tk.Label(
                form_frame, 
                text=label_text, 
                font=("Helvetica", 10),
                bg=self.bg_color
            )
            label.grid(row=i+1, column=0, sticky="e", padx=5, pady=5)
            
            if field_type == "entry":
                var = tk.StringVar(value=default_value)
                entry = tk.Entry(
                    form_frame,
                    font=("Helvetica", 10),
                    textvariable=var,
                    width=30
                )
                entry.grid(row=i+1, column=1, sticky="w", padx=5, pady=5)
                self.edit_product_vars[label_text] = var
            elif field_type == "text":
                text = tk.Text(
                    form_frame,
                    font=("Helvetica", 10),
                    width=30,
                    height=5,
                    wrap="word"
                )
                text.grid(row=i+1, column=1, sticky="w", padx=5, pady=5)
                text.insert("1.0", default_value)
                self.edit_product_vars[label_text] = text
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.bg_color)
        button_frame.grid(row=len(fields)+2, column=0, columnspan=2, pady=(20, 0))
        
        update_button = tk.Button(
            button_frame,
            text="Update Product",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=lambda: self.update_product(product_id, dialog)
        )
        update_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=10)
        
    def update_product(self, product_id, dialog):
        """Update existing product in inventory"""
        try:
            product = self.products[product_id]
            
            # Validate inputs
            name = self.edit_product_vars["Name:"].get().strip()
            category = self.edit_product_vars["Category:"].get().strip()
            description = self.edit_product_vars["Description:"].get("1.0", tk.END).strip()
            price_str = self.edit_product_vars["Price ($):"].get().strip()
            quantity_str = self.edit_product_vars["Quantity:"].get().strip()
            threshold_str = self.edit_product_vars["Low Stock Threshold:"].get().strip()
            supplier = self.edit_product_vars["Supplier:"].get().strip()
            
            if not all([name, category, price_str, quantity_str, threshold_str]):
                messagebox.showerror("Error", "Please fill in all required fields")
                return
            
            try:
                price = float(price_str)
                quantity = int(quantity_str)
                threshold = int(threshold_str)
                
                if price <= 0 or quantity < 0 or threshold < 0:
                    raise ValueError
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for price, quantity, and threshold")
                return
            
            # Record quantity change
            quantity_change = quantity - product["quantity"]
            
            # Update product in inventory
            self.products[product_id] = {
                "name": name,
                "category": category,
                "description": description,
                "price": price,
                "quantity": quantity,
                "threshold": threshold,
                "supplier": supplier,
                "created_at": product["created_at"],
                "modified_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Record transaction if quantity changed
            if quantity_change != 0:
                action_type = "add" if quantity_change > 0 else "remove"
                self.record_transaction(
                    product_id,
                    action_type,
                    abs(quantity_change),
                    f"Product {name} inventory updated"
                )
            
            # Save data
            self.save_data(self.products_file, self.products)
            
            # Refresh products list
            self.refresh_products_list()
            
            # Close dialog
            dialog.destroy()
            
            messagebox.showinfo("Success", f"Product {name} updated successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {str(e)}")

    def delete_product(self):
        """Delete selected product from inventory"""
        selected = self.products_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
            
        item = selected[0]
        product_id = self.products_tree.item(item)["values"][0]
        product_name = self.products[product_id]["name"]
        
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete product {product_name} (ID: {product_id})?"
        )
        
        if confirm:
            try:
                # Record transaction
                self.record_transaction(
                    product_id,
                    "remove",
                    self.products[product_id]["quantity"],
                    f"Product {product_name} deleted from inventory"
                )
                
                # Delete product
                del self.products[product_id]
                
                # Save data
                self.save_data(self.products_file, self.products)
                
                # Refresh products list
                self.refresh_products_list()
                
                messagebox.showinfo("Success", f"Product {product_name} deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def record_transaction(self, product_id, action, quantity, notes=""):
        """Record inventory transaction"""
        try:
            transaction_id = len(self.transactions) + 1
            
            self.transactions[f"T{transaction_id:05d}"] = {
                "product_id": product_id,
                "action": action,
                "quantity": quantity,
                "user": self.current_user,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "notes": notes
            }
            
            self.save_data(self.transactions_file, self.transactions)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to record transaction: {str(e)}")

    def show_inventory_tab(self):
        """Display inventory management tab"""
        # Clear tab content
        for widget in self.tab_content_frame.winfo_children():
            widget.destroy()
        
        # Inventory tab frame
        inventory_frame = tk.Frame(self.tab_content_frame, bg=self.bg_color)
        inventory_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Inventory header
        inventory_header = tk.Frame(inventory_frame, bg=self.bg_color)
        inventory_header.pack(fill="x", pady=(0, 10))
        
        inventory_label = tk.Label(
            inventory_header, 
            text="Inventory Operations", 
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color
        )
        inventory_label.pack(side="left")
        
        # Operations frame
        operations_frame = tk.Frame(inventory_frame, bg=self.bg_color)
        operations_frame.pack(fill="x", pady=(0, 20))
        
        # Section for stock operations
        stock_label = tk.Label(
            operations_frame,
            text="Stock Operations:",
            font=("Helvetica", 10, "bold"),
            bg=self.bg_color
        )
        stock_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Add stock button
        add_stock_button = tk.Button(
            operations_frame,
            text="Add Stock",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.add_stock_dialog
        )
        add_stock_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        # Remove stock button
        remove_stock_button = tk.Button(
            operations_frame,
            text="Remove Stock",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=self.remove_stock_dialog
        )
        remove_stock_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        # Section for low stock alert
        alert_label = tk.Label(
            operations_frame,
            text="Low Stock Report:",
            font=("Helvetica", 10, "bold"),
            bg=self.bg_color
        )
        alert_label.grid(row=2, column=0, sticky="w", pady=(20, 10))
        
        # Low stock report button
        low_stock_button = tk.Button(
            operations_frame,
            text="Generate Low Stock Report",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.generate_low_stock_report
        )
        low_stock_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Report display frame
        report_frame = tk.Frame(inventory_frame, bg=self.bg_color, bd=1, relief="sunken")
        report_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Report text widget
        self.report_text = tk.Text(
            report_frame,
            font=("Helvetica", 10),
            wrap="word",
            state="disabled",
            bg="white"
        )
        self.report_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Export button
        export_button = tk.Button(
            inventory_frame,
            text="Export to CSV",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.export_report_to_csv
        )
        export_button.pack(side="right", padx=5, pady=5)
        
        # Display current low stock alerts by default
        self.generate_low_stock_report()

    def generate_low_stock_report(self):
        """Generate report of products with low stock"""
        try:
            low_stock_products = []
            
            for product_id, product in self.products.items():
                if product["quantity"] <= product["threshold"]:
                    low_stock_products.append(product)
            
            self.report_text.configure(state="normal")
            self.report_text.delete("1.0", tk.END)
            
            if low_stock_products:
                self.report_text.insert("1.0", "LOW STOCK ALERT REPORT\n\n")
                self.report_text.insert("end", "The following products are below their minimum stock levels:\n\n")
                
                for product in sorted(low_stock_products, key=lambda x: x["quantity"]):
                    self.report_text.insert("end", f"Product ID: {product_id}\n")
                    self.report_text.insert("end", f"Name: {product['name']}\n")
                    self.report_text.insert("end", f"Current Stock: {product['quantity']}\n")
                    self.report_text.insert("end", f"Threshold: {product['threshold']}\n")
                    self.report_text.insert("end", f"Supplier: {product.get('supplier', 'N/A')}\n")
                    self.report_text.insert("end", "-" * 50 + "\n")
                    
            else:
                self.report_text.insert("1.0", "LOW STOCK REPORT\n\n")
                self.report_text.insert("end", "No products currently below minimum stock levels.\n")
                
            self.report_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def add_stock_dialog(self):
        """Show dialog for adding stock to a product"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Stock")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product selection
        product_label = tk.Label(
            form_frame,
            text="Select Product:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        product_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        self.add_stock_product_var = tk.StringVar()
        
        product_names = sorted([(product_id, f"{product_id} - {product['name']}") 
                              for product_id, product in self.products.items()], 
                              key=lambda x: x[1])
        
        product_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.add_stock_product_var,
            font=("Helvetica", 10),
            values=[name[1] for name in product_names],
            state="readonly",
            width=30
        )
        product_dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        product_dropdown.current(0)
        
        # Quantity to add
        quantity_label = tk.Label(
            form_frame,
            text="Quantity to Add:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        quantity_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.add_stock_quantity_var = tk.StringVar()
        
        quantity_entry = tk.Entry(
            form_frame,
            textvariable=self.add_stock_quantity_var,
            font=("Helvetica", 10),
            width=30
        )
        quantity_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Notes
        notes_label = tk.Label(
            form_frame,
            text="Notes:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        notes_label.grid(row=2, column=0, sticky="ne", padx=5, pady=5)
        
        self.add_stock_notes_var = tk.StringVar()
        
        notes_entry = tk.Entry(
            form_frame,
            textvariable=self.add_stock_notes_var,
            font=("Helvetica", 10),
            width=30
        )
        notes_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.bg_color)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        add_button = tk.Button(
            button_frame,
            text="Add Stock",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=lambda: self.add_stock(dialog)
        )
        add_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=10)
        
    def add_stock(self, dialog):
        """Add stock to selected product"""
        try:
            product_str = self.add_stock_product_var.get()
            product_id = product_str.split(" - ")[0]
            quantity_str = self.add_stock_quantity_var.get().strip()
            notes = self.add_stock_notes_var.get().strip()
            
            if not product_id or not quantity_str:
                messagebox.showerror("Error", "Please select a product and enter quantity")
                return
                
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive quantity")
                return
                
            product = self.products[product_id]
            product["quantity"] += quantity
            product["modified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Record transaction
            self.record_transaction(
                product_id,
                "add",
                quantity,
                f"Stock added: {notes}" if notes else "Stock added"
            )
            
            # Save data
            self.save_data(self.products_file, self.products)
            
            # Refresh products list if Products tab is active
            self.refresh_products_list()
            
            # Update low stock report if Inventory tab is active
            self.generate_low_stock_report()
            
            # Close dialog
            dialog.destroy()
            
            messagebox.showinfo("Success", f"{quantity} units added to {product['name']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add stock: {str(e)}")

    def remove_stock_dialog(self):
        """Show dialog for removing stock from a product"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Remove Stock")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product selection
        product_label = tk.Label(
            form_frame,
            text="Select Product:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        product_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        self.remove_stock_product_var = tk.StringVar()
        
        product_names = sorted([(product_id, f"{product_id} - {product['name']}") 
                              for product_id, product in self.products.items()], 
                              key=lambda x: x[1])
        
        product_dropdown = ttk.Combobox(
            form_frame,
            textvariable=self.remove_stock_product_var,
            font=("Helvetica", 10),
            values=[name[1] for name in product_names],
            state="readonly",
            width=30
        )
        product_dropdown.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        product_dropdown.current(0)
        
        # Current quantity display (readonly)
        current_label = tk.Label(
            form_frame,
            text="Current Quantity:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        current_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.current_quantity_var = tk.StringVar()
        self.current_quantity_var.set(self.products[product_names[0][0]]["quantity"])
        
        current_entry = tk.Entry(
            form_frame,
            textvariable=self.current_quantity_var,
            font=("Helvetica", 10),
            state="readonly",
            width=30
        )
        current_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Update current quantity when product selection changes
        def update_current_quantity(event):
            selected_product = self.remove_stock_product_var.get()
            if selected_product:
                product_id = selected_product.split(" - ")[0]
                self.current_quantity_var.set(self.products[product_id]["quantity"])
        
        product_dropdown.bind("<<ComboboxSelected>>", update_current_quantity)
        
        # Quantity to remove
        quantity_label = tk.Label(
            form_frame,
            text="Quantity to Remove:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        quantity_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        
        self.remove_stock_quantity_var = tk.StringVar()
        
        quantity_entry = tk.Entry(
            form_frame,
            textvariable=self.remove_stock_quantity_var,
            font=("Helvetica", 10),
            width=30
        )
        quantity_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Notes
        notes_label = tk.Label(
            form_frame,
            text="Notes:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        notes_label.grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        
        self.remove_stock_notes_var = tk.StringVar()
        
        notes_entry = tk.Entry(
            form_frame,
            textvariable=self.remove_stock_notes_var,
            font=("Helvetica", 10),
            width=30
        )
        notes_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.bg_color)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        remove_button = tk.Button(
            button_frame,
            text="Remove Stock",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=lambda: self.remove_stock(dialog)
        )
        remove_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=10)
        
    def remove_stock(self, dialog):
        """Remove stock from selected product"""
        try:
            product_str = self.remove_stock_product_var.get()
            product_id = product_str.split(" - ")[0]
            quantity_str = self.remove_stock_quantity_var.get().strip()
            notes = self.remove_stock_notes_var.get().strip()
            
            if not product_id or not quantity_str:
                messagebox.showerror("Error", "Please select a product and enter quantity")
                return
                
            try:
                quantity = int(quantity_str)
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive quantity")
                return
                
            product = self.products[product_id]
            
            if quantity > product["quantity"]:
                messagebox.showerror("Error", f"Not enough stock available. Current stock: {product['quantity']}")
                return
                
            product["quantity"] -= quantity
            product["modified_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Record transaction
            self.record_transaction(
                product_id,
                "remove",
                quantity,
                f"Stock removed: {notes}" if notes else "Stock removed"
            )
            
            # Save data
            self.save_data(self.products_file, self.products)
            
            # Refresh products list if Products tab is active
            self.refresh_products_list()
            
            # Update low stock report if Inventory tab is active
            self.generate_low_stock_report()
            
            # Close dialog
            dialog.destroy()
            
            messagebox.showinfo("Success", f"{quantity} units removed from {product['name']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove stock: {str(e)}")

    def show_reports_tab(self):
        """Display reports tab"""
        # Clear tab content
        for widget in self.tab_content_frame.winfo_children():
            widget.destroy()
        
        # Reports tab frame
        reports_frame = tk.Frame(self.tab_content_frame, bg=self.bg_color)
        reports_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Reports header
        reports_header = tk.Frame(reports_frame, bg=self.bg_color)
        reports_header.pack(fill="x", pady=(0, 10))
        
        reports_label = tk.Label(
            reports_header, 
            text="Reports Dashboard", 
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color
        )
        reports_label.pack(side="left")
        
        # Reports buttons frame
        buttons_frame = tk.Frame(reports_frame, bg=self.bg_color)
        buttons_frame.pack(fill="x", pady=(0, 10))
        
        sales_report_button = tk.Button(
            buttons_frame,
            text="Sales Summary Report",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            width=20,
            command=self.generate_sales_report
        )
        sales_report_button.pack(side="left", padx=5)
        
        inventory_report_button = tk.Button(
            buttons_frame,
            text="Inventory Report",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            width=20,
            command=self.generate_inventory_report
        )
        inventory_report_button.pack(side="left", padx=5)
        
        transactions_report_button = tk.Button(
            buttons_frame,
            text="Transactions Report",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            width=20,
            command=self.generate_transactions_report
        )
        transactions_report_button.pack(side="left", padx=5)
        
        # Report display frame
        report_display_frame = tk.Frame(
            reports_frame,
            bg=self.bg_color,
            bd=1,
            relief="sunken"
        )
        report_display_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Report text widget
        self.report_display_text = tk.Text(
            report_display_frame,
            font=("Courier", 10),
            wrap="none",
            state="disabled",
            bg="white"
        )
        self.report_display_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(
            report_display_frame,
            orient="horizontal",
            command=self.report_display_text.xview
        )
        h_scrollbar.pack(fill="x", padx=5)
        self.report_display_text.configure(xscrollcommand=h_scrollbar.set)
        
        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(
            report_display_frame,
            command=self.report_display_text.yview
        )
        v_scrollbar.pack(side="right", fill="y", padx=(0, 5))
        self.report_display_text.configure(yscrollcommand=v_scrollbar.set)
        
        # Export button
        export_report_button = tk.Button(
            reports_frame,
            text="Export Report to CSV",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.export_report_to_csv
        )
        export_report_button.pack(side="right", padx=5, pady=5)
        
        # Generate sales report by default
        self.generate_sales_report()

    def generate_sales_report(self):
        """Generate sales summary report"""
        try:
            self.report_display_text.configure(state="normal")
            self.report_display_text.delete("1.0", tk.END)
            
            # Prepare data
            product_value = {}
            total_value = 0
            
            for product_id, product in self.products.items():
                value = product["price"] * product["quantity"]
                product_value[product_id] = value
                total_value += value
            
            # Sort products by value (descending)
            sorted_products = sorted(self.products.items(), 
                                   key=lambda x: product_value[x[0]], 
                                   reverse=True)
            
            # Generate report
            report_title = "SALES SUMMARY REPORT\n"
            self.report_display_text.insert("1.0", report_title)
            
            # Current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.report_display_text.insert("end", f"\nGenerated on: {timestamp}\n")
            
            # Report header
            self.report_display_text.insert("end", "\n")
            self.report_display_text.insert("end", f"{'-'*85}\n")
            self.report_display_text.insert("end", 
                "| {:<10} | {:<30} | {:<10} | {:<10} | {:<10} |\n".format(
                    "Product ID", "Product Name", "Price ($)", "Quantity", "Value ($)"
                )
            )
            self.report_display_text.insert("end", f"{'-'*85}\n")
            
            # Product data
            for product_id, product in sorted_products:
                self.report_display_text.insert("end", 
                    "| {:<10} | {:<30} | {:<10.2f} | {:<10} | {:<10.2f} |\n".format(
                        product_id,
                        product["name"],
                        product["price"],
                        product["quantity"],
                        product_value[product_id]
                    )
                )
            
            # Footer with totals
            self.report_display_text.insert("end", f"{'-'*85}\n")
            self.report_display_text.insert("end", 
                "| {:<42} | {:<10} | {:<10} | {:<10.2f} |\n".format(
                    "",
                    "",
                    "",
                    total_value
                )
            )
            self.report_display_text.insert("end", f"{'-'*85}\n")
            
            self.report_display_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate sales report: {str(e)}")

    def generate_inventory_report(self):
        """Generate inventory summary report"""
        try:
            self.report_display_text.configure(state="normal")
            self.report_display_text.delete("1.0", tk.END)
            
            # Prepare data - count products per category
            categories = {}
            for product in self.products.values():
                category = product["category"]
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            # Sort categories alphabetically
            sorted_categories = sorted(categories.items())
            
            # Generate report
            report_title = "INVENTORY CATEGORY REPORT\n"
            self.report_display_text.insert("1.0", report_title)
            
            # Current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.report_display_text.insert("end", f"\nGenerated on: {timestamp}\n")
            
            # Report header
            self.report_display_text.insert("end", "\n")
            self.report_display_text.insert("end", f"{'-'*45}\n")
            self.report_display_text.insert("end", 
                "| {:<25} | {:<15} |\n".format("Category", "Product Count")
            )
            self.report_display_text.insert("end", f"{'-'*45}\n")
            
            # Category data
            for category, count in sorted_categories:
                self.report_display_text.insert("end", 
                    "| {:<25} | {:<15} |\n".format(category, count)
                )
            
            # Footer with totals
            self.report_display_text.insert("end", f"{'-'*45}\n")
            self.report_display_text.insert("end", 
                "| {:<25} | {:<15} |\n".format("TOTAL", len(self.products))
            )
            self.report_display_text.insert("end", f"{'-'*45}\n")
            
            self.report_display_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate inventory report: {str(e)}")

    def generate_transactions_report(self):
        """Generate transactions summary report"""
        try:
            self.report_display_text.configure(state="normal")
            self.report_display_text.delete("1.0", tk.END)
            
            # Generate report
            report_title = "TRANSACTIONS REPORT\n"
            self.report_display_text.insert("1.0", report_title)
            
            # Current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.report_display_text.insert("end", f"\nGenerated on: {timestamp}\n")
            
            if not self.transactions:
                self.report_display_text.insert("end", "\nNo transactions recorded yet.\n")
                self.report_display_text.configure(state="disabled")
                return
            
            # Report header
            self.report_display_text.insert("end", "\n")
            self.report_display_text.insert("end", f"{'-'*100}\n")
            self.report_display_text.insert("end", 
                "| {:<10} | {:<15} | {:<20} | {:<15} | {:<10} | {:<20} |\n".format(
                    "Trx ID", "Product ID", "Action", "Quantity", "User", "Timestamp"
                )
            )
            self.report_display_text.insert("end", f"{'-'*100}\n")
            
            # Transaction data (sorted by timestamp)
            sorted_transactions = sorted(self.transactions.items(), 
                                       key=lambda x: x[1]["timestamp"], 
                                       reverse=True)
            
            for trx_id, trx in sorted_transactions:
                product_id = trx["product_id"]
                
                # Get product name if possible
                product_name = ""
                if product_id in self.products:
                    product_name = self.products[product_id]["name"]
                
                self.report_display_text.insert("end", 
                    "| {:<10} | {:<15} | {:<20} | {:<15} | {:<10} | {:<20} |\n".format(
                        trx_id,
                        product_id,
                        trx["action"],
                        trx["quantity"],
                        trx["user"],
                        trx["timestamp"]
                    )
                )
                
                # Add notes if available
                if trx.get("notes"):
                    self.report_display_text.insert("end", 
                        "| {:<10} | Notes: {:<85} |\n".format("", trx["notes"])
                    )
                    
                self.report_display_text.insert("end", f"{'-'*100}\n")
            
            self.report_display_text.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate transactions report: {str(e)}")

    def export_report_to_csv(self):
        """Export current report to CSV file"""
        try:
            # Get the current report contents
            if hasattr(self, "report_text"):
                report_contents = self.report_text.get("1.0", tk.END)
                default_filename = "low_stock_report.csv"
            elif hasattr(self, "report_display_text"):
                report_contents = self.report_display_text.get("1.0", tk.END)
                default_filename = "inventory_report.csv"
            else:
                messagebox.showwarning("Warning", "No report currently displayed to export")
                return
                
            # Ask user for file location
            file_path = simpledialog.askstring(
                "Export Report",
                "Enter filename to save:",
                initialvalue=default_filename
            )
            
            if not file_path:
                return
                
            # Ensure .csv extension
            if not file_path.lower().endswith('.csv'):
                file_path += '.csv'
                
            # Write report to CSV file
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Split lines and write each as a row
                lines = report_contents.split('\n')
                for line in lines:
                    if line.strip():  # Skip empty lines
                        writer.writerow([line])
            
            messagebox.showinfo("Success", f"Report successfully exported to {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")

    def show_users_tab(self):
        """Display user management tab"""
        # Clear tab content
        for widget in self.tab_content_frame.winfo_children():
            widget.destroy()
        
        # Users tab frame
        users_frame = tk.Frame(self.tab_content_frame, bg=self.bg_color)
        users_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Users header
        users_header = tk.Frame(users_frame, bg=self.bg_color)
        users_header.pack(fill="x", pady=(0, 10))
        
        users_label = tk.Label(
            users_header, 
            text="User Management", 
            font=("Helvetica", 12, "bold"),
            bg=self.bg_color
        )
        users_label.pack(side="left")
        
        add_user_button = tk.Button(
            users_header, 
            text="Add User", 
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.add_user_dialog
        )
        add_user_button.pack(side="right", padx=5)
        
        # Users treeview
        self.users_tree = ttk.Treeview(
            users_frame,
            columns=("username", "role"),
            show="headings",
            selectmode="browse"
        )
        
        # Configure columns
        self.users_tree.heading("username", text="Username", anchor="w")
        self.users_tree.heading("role", text="Role", anchor="w")
        
        self.users_tree.column("username", width=200)
        self.users_tree.column("role", width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        self.users_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Action buttons frame
        action_frame = tk.Frame(users_frame, bg=self.bg_color)
        action_frame.pack(fill="x", pady=(10, 0))
        
        reset_password_button = tk.Button(
            action_frame,
            text="Reset Password",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.reset_password_dialog
        )
        reset_password_button.pack(side="left", padx=5)
        
        delete_user_button = tk.Button(
            action_frame,
            text="Delete User",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=self.delete_user
        )
        delete_user_button.pack(side="left", padx=5)
        
        refresh_users_button = tk.Button(
            action_frame,
            text="Refresh",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=self.refresh_users_list
        )
        refresh_users_button.pack(side="right", padx=5)
        
        # Populate users tree
        self.refresh_users_list()

    def refresh_users_list(self):
        """Refresh the users treeview with current data"""
        self.users_tree.delete(*self.users_tree.get_children())
        
        # Sort users alphabetically
        sorted_users = sorted(self.users.items(), key=lambda x: x[0])
        
        for username, user_data in sorted_users:
            self.users_tree.insert(
                "", 
                "end", 
                values=(
                    username,
                    user_data["role"]
                )
            )

    def add_user_dialog(self):
        """Show dialog for adding new user"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New User")
        dialog.geometry("300x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Username
        username_label = tk.Label(
            form_frame,
            text="Username:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        username_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        self.new_username_var = tk.StringVar()
        
        username_entry = tk.Entry(
            form_frame,
            textvariable=self.new_username_var,
            font=("Helvetica", 10),
            width=25
        )
        username_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Password
        password_label = tk.Label(
            form_frame,
            text="Password:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        password_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.new_password_var = tk.StringVar()
        
        password_entry = tk.Entry(
            form_frame,
            textvariable=self.new_password_var,
            font=("Helvetica", 10),
            width=25,
            show="*"
        )
        password_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Confirm Password
        confirm_label = tk.Label(
            form_frame,
            text="Confirm Password:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        confirm_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
        
        self.confirm_password_var = tk.StringVar()
        
        confirm_entry = tk.Entry(
            form_frame,
            textvariable=self.confirm_password_var,
            font=("Helvetica", 10),
            width=25,
            show="*"
        )
        confirm_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Role
        role_label = tk.Label(
            form_frame,
            text="Role:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        role_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        
        self.new_role_var = tk.StringVar(value="staff")
        
        role_admin = tk.Radiobutton(
            form_frame,
            text="Admin",
            variable=self.new_role_var,
            value="admin",
            bg=self.bg_color,
            font=("Helvetica", 10)
        )
        role_admin.grid(row=3, column=1, sticky="w", padx=5)
        
        role_staff = tk.Radiobutton(
            form_frame,
            text="Staff",
            variable=self.new_role_var,
            value="staff",
            bg=self.bg_color,
            font=("Helvetica", 10)
        )
        role_staff.grid(row=4, column=1, sticky="w", padx=5)
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.bg_color)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        add_button = tk.Button(
            button_frame,
            text="Add User",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=lambda: self.add_user(dialog)
        )
        add_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=10)

    def add_user(self, dialog):
        """Add new user"""
        try:
            username = self.new_username_var.get().strip()
            password = self.new_password_var.get().strip()
            confirm_password = self.confirm_password_var.get().strip()
            role = self.new_role_var.get()
            
            if not all([username, password, confirm_password]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
                
            if username in self.users:
                messagebox.showerror("Error", "Username already exists")
                return
                
            # Create new user
            self.users[username] = {
                "password": password,
                "role": role
            }
            
            # Save data
            self.save_data(self.users_file, self.users)
            
            # Refresh users list
            self.refresh_users_list()
            
            # Close dialog
            dialog.destroy()
            
            messagebox.showinfo("Success", f"User {username} added successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add user: {str(e)}")

    def reset_password_dialog(self):
        """Show dialog for resetting user password"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to reset password")
            return
            
        item = selected[0]
        username = self.users_tree.item(item)["values"][0]
        
        # Don't allow changing admin password unless current user is admin
        if username == "admin" and self.current_user != "admin":
            messagebox.showerror("Error", "Only admin can change the admin password")
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Reset Password for {username}")
        dialog.geometry("300x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Form frame
        form_frame = tk.Frame(dialog, bg=self.bg_color)
        form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # New Password
        password_label = tk.Label(
            form_frame,
            text="New Password:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        password_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        self.reset_password_var = tk.StringVar()
        
        password_entry = tk.Entry(
            form_frame,
            textvariable=self.reset_password_var,
            font=("Helvetica", 10),
            width=25,
            show="*"
        )
        password_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Confirm Password
        confirm_label = tk.Label(
            form_frame,
            text="Confirm Password:",
            font=("Helvetica", 10),
            bg=self.bg_color
        )
        confirm_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.confirm_reset_password_var = tk.StringVar()
        
        confirm_entry = tk.Entry(
            form_frame,
            textvariable=self.confirm_reset_password_var,
            font=("Helvetica", 10),
            width=25,
            show="*"
        )
        confirm_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Button frame
        button_frame = tk.Frame(form_frame, bg=self.bg_color)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        reset_button = tk.Button(
            button_frame,
            text="Reset Password",
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg="white",
            command=lambda: self.reset_password(username, dialog)
        )
        reset_button.pack(side="left", padx=10)
        
        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Helvetica", 10),
            bg=self.accent_color,
            fg="white",
            command=dialog.destroy
        )
        cancel_button.pack(side="left", padx=10)

    def reset_password(self, username, dialog):
        """Reset user password"""
        try:
            password = self.reset_password_var.get().strip()
            confirm_password = self.confirm_reset_password_var.get().strip()
            
            if not all([password, confirm_password]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
                
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
                
            # Update user password
            self.users[username]["password"] = password
            
            # Save data
            self.save_data(self.users_file, self.users)
            
            # Close dialog
            dialog.destroy()
            
            messagebox.showinfo("Success", f"Password for {username} reset successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reset password: {str(e)}")

    def delete_user(self):
        """Delete selected user"""
        selected = self.users_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
            
        item = selected[0]
        username = self.users_tree.item(item)["values"][0]
        
        if username == "admin":
            messagebox.showerror("Error", "Cannot delete admin account")
            return
            
        if username == self.current_user:
            messagebox.showerror("Error", "Cannot delete your own account")
            return
            
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete user {username}?"
        )
        
        if confirm:
            try:
                # Delete user
                del self.users[username]
                
                # Save data
                self.save_data(self.users_file, self.users)
                
                # Refresh users list
                self.refresh_users_list()
                
                messagebox.showinfo("Success", f"User {username} deleted successfully")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")
    def on_closing(self):
        self.save_data(self.products_file,self.products)
        self.save_data(self.users_file,self.users)
        self.save_data(self.transactions_file,self.transactions)
        if messagebox.askokcancel("Quit","Do you want to quit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    
    # Set window icon (optional - replace with actual icon file if needed)
    try:
        root.iconbitmap("inventory_icon.ico")
    except:
        pass
    
    # Bind keyboard shortcuts
    root.bind("<F1>", lambda event: app.show_help())
    root.bind("<Control-q>", lambda event: app.on_closing())
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()