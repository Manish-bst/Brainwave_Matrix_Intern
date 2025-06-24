import tkinter as tk
from tkinter import messagebox
import json, random
from datetime import datetime

class SimpleATM:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM Simulator")
        self.root.geometry("500x700")  # Increased height
        self.root.resizable(False, False)
        
        # Colors
        self.bg_color = "#2c3e50"
        self.button_color = "#3498db"
        self.text_color = "#ecf0f1"
        self.screen_color = "#34495e"
        
        # Configure root window
        self.root.configure(bg=self.bg_color)
        
        # Load data
        self.data_file = "atm_data.json"
        self.default_data = {
            "pin": "1234",
            "balance": 1000,
            "transactions": []
        }
        self.load_data()
        
        # Create widgets
        self.create_widgets()
        
        # Start with PIN entry
        self.pin_mode()

    def load_data(self):
        try:
            with open(self.data_file, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = self.default_data
            self.save_data()
    
    def save_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, indent=4)

    def create_widgets(self):
        # Header
        self.header = tk.Label(self.root, text="ATM SIMULATOR", 
                             font=("Arial", 20, "bold"),
                             bg=self.bg_color, fg=self.text_color)
        self.header.pack(pady=10)
        
        # Screen
        self.screen = tk.Text(self.root, height=12, width=50,
                            font=("Courier New", 12),
                            bg=self.screen_color, fg=self.text_color,
                            state=tk.DISABLED)
        self.screen.pack(pady=10, padx=20)
        
        # Operation buttons (now above keypad)
        self.ops_frame = tk.Frame(self.root, bg=self.bg_color)
        self.ops_frame.pack(pady=10)
        
        self.ops_buttons = []
        operations = [
            ("Balance", self.check_balance),
            ("Withdraw", self.withdraw_menu),
            ("Deposit", self.deposit_menu),
            ("Change PIN", self.change_pin_menu),
            ("Statement", self.show_statement)
        ]
        
        for text, command in operations:
            btn = tk.Button(self.ops_frame, text=text, width=10,
                          font=("Arial", 10),
                          bg=self.button_color, fg="white",
                          command=command)
            btn.pack(side=tk.LEFT, padx=5)
            self.ops_buttons.append(btn)
        
        # Hide operation buttons initially
        self.ops_frame.pack_forget()
        
        # Keypad (now below operations)
        self.keypad_frame = tk.Frame(self.root, bg=self.bg_color)
        self.keypad_frame.pack()
        
        buttons = [
            ("1", "2", "3"),
            ("4", "5", "6"),
            ("7", "8", "9"),
            ("Clear", "0", "Enter")
        ]
        
        for row in buttons:
            row_frame = tk.Frame(self.keypad_frame, bg=self.bg_color)
            row_frame.pack()
            for text in row:
                btn = tk.Button(row_frame, text=text, width=8, height=2,
                              font=("Arial", 12),
                              bg=self.button_color, fg="white",
                              command=lambda t=text: self.on_button_click(t))
                btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Exit button at bottom
        self.exit_btn = tk.Button(self.root, text="Exit", width=10,
                                font=("Arial", 12),
                                bg="#e74c3c", fg="white",
                                command=self.exit_atm)
        self.exit_btn.pack(pady=10)
        self.exit_btn.pack_forget()

    def pin_mode(self):
        self.clear_screen()
        self.print_to_screen("Please enter your 4-digit PIN:")
        self.entered_pin = ""
        self.current_mode = "pin_entry"
        self.ops_frame.pack_forget()
        self.exit_btn.pack_forget()

    def menu_mode(self):
        self.clear_screen()
        self.print_to_screen("Select an operation:")
        self.current_mode = "menu"
        self.ops_frame.pack()
        self.exit_btn.pack(pady=10)

    def print_to_screen(self, text):
        self.screen.config(state=tk.NORMAL)
        self.screen.insert(tk.END, text + "\n")
        self.screen.see(tk.END)
        self.screen.config(state=tk.DISABLED)

    def clear_screen(self):
        self.screen.config(state=tk.NORMAL)
        self.screen.delete(1.0, tk.END)
        self.screen.config(state=tk.DISABLED)

    def generate_captcha(self):
        return str(random.randint(1000, 9999))

    def on_button_click(self, text):
        if self.current_mode == "pin_entry":
            self.handle_pin_entry(text)
        elif self.current_mode == "withdraw":
            self.handle_withdraw(text)
        elif self.current_mode == "deposit":
            self.handle_deposit(text)
        elif self.current_mode == "change_pin1":
            self.handle_old_pin_entry(text)
        elif self.current_mode == "change_pin2":
            self.handle_new_pin_entry(text)
        elif self.current_mode == "change_pin3":
            self.handle_confirm_pin_entry(text)
        elif self.current_mode == "captcha":
            self.handle_captcha_entry(text)

    def handle_pin_entry(self, text):
        if text == "Clear":
            self.entered_pin = ""
            self.clear_screen()
            self.print_to_screen("Please enter your 4-digit PIN:")
        elif text == "Enter":
            if len(self.entered_pin) == 4:
                if self.entered_pin == self.data["pin"]:
                    self.menu_mode()
                else:
                    messagebox.showerror("Error", "Incorrect PIN")
                    self.pin_mode()
            else:
                messagebox.showerror("Error", "PIN must be 4 digits")
                self.pin_mode()
        elif text.isdigit() and len(self.entered_pin) < 4:
            self.entered_pin += text
            self.print_to_screen("*" * len(self.entered_pin))

    def handle_withdraw(self, text):
        if text == "Clear":
            self.amount_entry = ""
            self.clear_screen()
            self.print_to_screen("Enter withdrawal amount:")
        elif text == "Enter":
            if self.amount_entry:
                self.process_withdrawal(int(self.amount_entry))
        elif text.isdigit():
            self.amount_entry += text
            self.print_to_screen(self.amount_entry)

    def handle_deposit(self, text):
        if text == "Clear":
            self.amount_entry = ""
            self.clear_screen()
            self.print_to_screen("Enter deposit amount:")
        elif text == "Enter":
            if self.amount_entry:
                self.process_deposit(int(self.amount_entry))
        elif text.isdigit():
            self.amount_entry += text
            self.print_to_screen(self.amount_entry)

    def handle_old_pin_entry(self, text):
        if text == "Clear":
            self.old_pin = ""
            self.clear_screen()
            self.print_to_screen("Enter current PIN:")
        elif text == "Enter":
            if len(self.old_pin) == 4:
                if self.old_pin == self.data["pin"]:
                    self.current_mode = "change_pin2"
                    self.clear_screen()
                    self.print_to_screen("Enter new 4-digit PIN:")
                    self.new_pin = ""
                else:
                    messagebox.showerror("Error", "Incorrect current PIN")
                    self.menu_mode()
            else:
                messagebox.showerror("Error", "PIN must be 4 digits")
                self.menu_mode()
        elif text.isdigit() and len(self.old_pin) < 4:
            self.old_pin += text
            self.print_to_screen("*" * len(self.old_pin))

    def handle_new_pin_entry(self, text):
        if text == "Clear":
            self.new_pin = ""
            self.clear_screen()
            self.print_to_screen("Enter new 4-digit PIN:")
        elif text == "Enter":
            if len(self.new_pin) == 4:
                self.current_mode = "change_pin3"
                self.clear_screen()
                self.print_to_screen("Confirm new 4-digit PIN:")
                self.confirm_pin = ""
            else:
                messagebox.showerror("Error", "PIN must be 4 digits")
                self.menu_mode()
        elif text.isdigit() and len(self.new_pin) < 4:
            self.new_pin += text
            self.print_to_screen("*" * len(self.new_pin))

    def handle_confirm_pin_entry(self, text):
        if text == "Clear":
            self.confirm_pin = ""
            self.clear_screen()
            self.print_to_screen("Confirm new 4-digit PIN:")
        elif text == "Enter":
            if len(self.confirm_pin) == 4:
                if self.new_pin == self.confirm_pin:
                    # Generate CAPTCHA before final change
                    self.current_mode = "captcha"
                    self.captcha_code = self.generate_captcha()
                    self.clear_screen()
                    self.print_to_screen(f"Enter this CAPTCHA: {self.captcha_code}")
                    self.entered_captcha = ""
                else:
                    messagebox.showerror("Error", "PINs don't match")
                    self.menu_mode()
            else:
                messagebox.showerror("Error", "PIN must be 4 digits")
                self.menu_mode()
        elif text.isdigit() and len(self.confirm_pin) < 4:
            self.confirm_pin += text
            self.print_to_screen("*" * len(self.confirm_pin))

    def handle_captcha_entry(self, text):
        if text == "Clear":
            self.entered_captcha = ""
            self.clear_screen()
            self.print_to_screen(f"Enter this CAPTCHA: {self.captcha_code}")
        elif text == "Enter":
            if self.entered_captcha == self.captcha_code:
                self.data["pin"] = self.new_pin
                self.save_data()
                messagebox.showinfo("Success", "PIN changed successfully!")
                self.record_transaction("PIN Changed")
                self.menu_mode()
            else:
                messagebox.showerror("Error", "Incorrect CAPTCHA")
                self.menu_mode()
        elif text.isdigit() and len(self.entered_captcha) < 4:
            self.entered_captcha += text
            self.print_to_screen(self.entered_captcha)

    def check_balance(self):
        self.clear_screen()
        self.print_to_screen(f"Current Balance: ${self.data['balance']}")
        self.record_transaction("Balance Check")

    def withdraw_menu(self):
        self.clear_screen()
        self.print_to_screen("Enter withdrawal amount:")
        self.amount_entry = ""
        self.current_mode = "withdraw"

    def process_withdrawal(self, amount):
        if amount % 100 != 0:
            messagebox.showerror("Error", "Amount must be in multiples of $100")
        elif amount > (self.data['balance'] - 100):
            messagebox.showerror("Error", "Insufficient funds")
        else:
            self.data['balance'] -= amount
            self.save_data()
            self.clear_screen()
            self.print_to_screen(f"Withdrew: ${amount}")
            self.print_to_screen(f"New balance: ${self.data['balance']}")
            self.record_transaction(f"Withdrawal: ${amount}")
            self.current_mode = "menu"

    def deposit_menu(self):
        self.clear_screen()
        self.print_to_screen("Enter deposit amount:")
        self.amount_entry = ""
        self.current_mode = "deposit"

    def process_deposit(self, amount):
        self.data['balance'] += amount
        self.save_data()
        self.clear_screen()
        self.print_to_screen(f"Deposited: ${amount}")
        self.print_to_screen(f"New balance: ${self.data['balance']}")
        self.record_transaction(f"Deposit: ${amount}")
        self.current_mode = "menu"

    def change_pin_menu(self):
        self.clear_screen()
        self.print_to_screen("Enter current PIN:")
        self.old_pin = ""
        self.current_mode = "change_pin1"

    def show_statement(self):
        self.clear_screen()
        self.print_to_screen("=== Last 5 Transactions ===")
        transactions = self.data['transactions'][-5:][::-1]  # Last 5 reversed
        
        if not transactions:
            self.print_to_screen("No transactions yet")
        else:
            for txn in transactions:
                date = datetime.strptime(txn['date'], "%Y-%m-%d %H:%M:%S").strftime("%m/%d %H:%M")
                self.print_to_screen(f"{date}: {txn['type']}")
                self.print_to_screen(f"Balance: ${txn['balance']}")
                self.print_to_screen("-"*40)
        
        self.print_to_screen(f"Current Balance: ${self.data['balance']}")
        self.record_transaction("Statement Viewed")

    def record_transaction(self, transaction_type):
        transaction = {
            "type": transaction_type,
            "balance": self.data['balance'],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data['transactions'].append(transaction)
        if len(self.data['transactions']) > 20:
            self.data['transactions'] = self.data['transactions'][-20:]
        self.save_data()

    def exit_atm(self):
        self.clear_screen()
        self.print_to_screen("Thank you for using")
        self.print_to_screen("our ATM service!")
        self.root.after(1500, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    atm = SimpleATM(root)
    root.mainloop()
