import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
import os
import re
import json


from Authorization import Authorization
from DataManager import DataManager
from Functions import Functions


# Thiết lập biến môi trường PYDEVD_DISABLE_FILE_VALIDATION
os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

# Thiết lập biến môi trường PYDEVD_USE_CYTHON=1 để hỗ trợ frozen_modules
os.environ["PYDEVD_USE_CYTHON"] = "1"

BG_TOP_FRAME = "#f7f9fc"
BG_MIDDLE_FRAME = "#e2e8f0"
BG_BOTTOM_FRAME = "#e2e8f0"
BTN_COLOR = "#4a90e2"
BTN_TEXT_COLOR = "white"
BTN_HOVER_COLOR = "#357ab7"
TEXT_COLOR = "#2d3748"
HEADING_COLOR = "#1a202c"

NUM_OF_ROW = 2
NUM_OF_COLUMN = 1

BASE_DIR = os.path.dirname(__file__)
LOGO_PATH = os.path.join(BASE_DIR, "icon", "logo.png")
LOGO_IMAGE = Image.open(LOGO_PATH)

date = datetime.now().date()
date = str(date)


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.authorization = Authorization()
        self.dataManager = DataManager()

        self.user_json_path = os.path.join(BASE_DIR, "user.json")

        self.logo_photo = ImageTk.PhotoImage(LOGO_IMAGE)

        self.root.iconphoto(True, self.logo_photo)
        self.root.title("Login")
        self.root.geometry("400x300+500+200")

        self.create_login_frame()

        self.root.mainloop()

    def create_login_frame(self):
        self.login_frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.SOLID)
        self.login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.title_label = tk.Label(
            self.login_frame,
            text="Login",
            font=("Helvetica", 16, "bold"),
            bg="#ffffff",
        )
        self.title_label.grid(row=0, columnspan=2, pady=10)

        self.username_label = tk.Label(
            self.login_frame,
            text="Username:",
            font=("Helvetica", 12),
            bg="#ffffff",
        )
        self.username_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.username_entry.grid(row=1, column=1, padx=10, pady=5)

        self.password_label = tk.Label(
            self.login_frame,
            text="Password:",
            font=("Helvetica", 12),
            bg="#ffffff",
        )
        self.password_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.password_entry = tk.Entry(
            self.login_frame, show="*", font=("Helvetica", 12)
        )
        self.password_entry.grid(row=2, column=1, padx=10, pady=5)

        self.show_password = False

        open_eye_path = os.path.join(BASE_DIR, "icon", "open_eye.png")
        self.open_eye_image = Image.open(open_eye_path)
        self.open_eye_image = self.open_eye_image.resize((20, 20), Image.LANCZOS)
        self.open_eye_photo = ImageTk.PhotoImage(self.open_eye_image)

        close_eye_path = os.path.join(BASE_DIR, "icon", "close_eye.png")
        self.close_eye_image = Image.open(close_eye_path)
        self.close_eye_image = self.close_eye_image.resize((20, 20), Image.LANCZOS)
        self.close_eye_photo = ImageTk.PhotoImage(self.close_eye_image)

        self.eye_button = tk.Button(
            self.login_frame,
            image=self.close_eye_photo,
            command=self.toggle_password_visibility,
            bd=0,
            bg="#ffffff",
            activebackground="#ffffff",
        )
        self.eye_button.grid(row=2, column=2, padx=5)

        self.login_button = tk.Button(
            self.login_frame,
            text="Login",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="#ffffff",
            activebackground="#45a049",
            activeforeground="#ffffff",
            command=self.login,
            width=10
        )
        self.login_button.grid(row=3, columnspan=3, pady=20)
        
        self.sign_up_label = tk.Label(self.login_frame, text="You don't have account?",font=("Helvetica", 8, "bold"))
        self.sign_up_label.grid(row=4, column=1, pady=10)
        self.sign_up_button = tk.Button(
            self.login_frame,
            text="Sign up",
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="#ffffff",
            activebackground="#45a049",
            activeforeground="#ffffff",
            command=self.sign_up,
        )
        self.sign_up_button.grid(row=4, column=2, pady=10)

    def toggle_password_visibility(self):
        if self.show_password:
            self.password_entry.config(show="*")
            self.eye_button.config(image=self.close_eye_photo)
            self.show_password = False
        else:
            self.password_entry.config(show="")
            self.eye_button.config(image=self.open_eye_photo)
            self.show_password = True

    def login(self):
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.authorization.login(self.username, password)
        if role == "admin":
            self.role = role
            self.login_frame.destroy()
            self.root.destroy()
            self.show_main_menu_admin()
        elif role == "user":
            self.role = role
            self.login_frame.destroy()
            self.root.destroy()
            self.show_main_menu_user()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def sign_up(self):
        self.sign_up_window = tk.Toplevel(self.root)
        
        self.sign_up_window.title("Sign up")
        self.sign_up_window.geometry("320x200+500+200")
        
        self.sign_up_username_label = tk.Label(self.sign_up_window, text="Tên tài khoản:", bg="white")
        self.sign_up_username_label.grid(row=0, column=0, padx=5, pady=5)
        self.sign_up_username_entry = tk.Entry(self.sign_up_window)
        self.sign_up_username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.sign_up_password_label = tk.Label(self.sign_up_window, text="Mật khẩu:", bg="white")
        self.sign_up_password_label.grid(row=1, column=0, padx=5, pady=5)
        self.sign_up_password_entry = tk.Entry(self.sign_up_window, show="*")
        self.sign_up_password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.sign_up_confirm_password_label = tk.Label(
            self.sign_up_window, text="Nhập lại mật khẩu:", bg="white"
        )
        self.sign_up_confirm_password_label.grid(row=2, column=0, padx=5, pady=5)
        self.sign_up_confirm_password_entry = tk.Entry(self.sign_up_window, show="*")
        self.sign_up_confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.sign_up_role_label = tk.Label(self.sign_up_window, text="Vai trò:", bg="white")
        self.sign_up_role_label.grid(row=3, column=0, padx=5, pady=5)
        self.sign_up_role_var = tk.StringVar()
        self.sign_up_role_var.set("user")
        self.sign_up_user_radio = tk.Radiobutton(
            self.sign_up_window, text="User", variable=self.sign_up_role_var, value="user", bg="white"
        )
        self.sign_up_user_radio.grid(row=3, column=1, padx=5, pady=5)
        self.sign_up_admin_radio = tk.Radiobutton(
            self.sign_up_window, text="Admin", variable=self.sign_up_role_var, value="admin", bg="white"
        )
        self.sign_up_admin_radio.grid(row=3, column=2, padx=5, pady=5)
        
        self.sign_up_create_button = tk.Button(
            self.sign_up_window, text="Tạo mới", command=self.create_user, width=10
        )
        self.sign_up_create_button.grid(row=4,column=1,padx=5, pady=5)
        
        self.sign_up_exit_button = tk.Button(
            self.sign_up_window, text="Thoát", command=lambda : self.close_window(self.sign_up_window), width=10
        )
        self.sign_up_exit_button.grid(row=5,column=1,padx=5, pady=5)
    
    def create_user(self):
        username = self.sign_up_username_entry.get()
        password = self.sign_up_password_entry.get()
        confirm_password = self.sign_up_confirm_password_entry.get()
        
        if self.is_exist_username(username):
            messagebox.showerror("Lỗi", "Tên tài khoản đã tồn tại")
            return

        if not username or not password:
            messagebox.showerror("Error", "Vui lòng nhập tên tài khoản và mật khẩu.")
            return

        if not self.validate_username(username):
            return

        if not self.validate_password(password, confirm_password):
            return

        for user in self.authorization.user_list:
            if user["username"] == username:
                messagebox.showerror("Error", "Tài khoản đã tồn tại.")
                return

        new_user = {
            "username": username,
            "password": password,
            "role": self.sign_up_role_var.get(),
        }
        self.authorization.user_list.append(new_user)
        self.save_users()
        messagebox.showinfo("Success", "Tạo tài khoản thành công!")
        self.clear_entries()
        self.close_window(self.sign_up_window)

    def is_exist_username(self, username):
        
        for account in self.authorization.user_list:
            if username == account["username"]:
                return True
        return False
    
    # Hàm kiểm tra mật khẩu
    def validate_password(self, password, confirm_password):
        if password != confirm_password:
            messagebox.showerror("Error", "Mật khẩu nhập lại không khớp.")
            return False
        if (
            len(password) < 8
            or not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
            or not re.search(r"[#@_$%^&+=]", password)
        ):
            messagebox.showerror(
                "Error",
                "Mật khẩu phải có ít nhất 8 ký tự, bao gồm 1 ký tự in hoa, 1 ký tự thường, 1 số, và 1 ký tự đặc biệt.",
            )
            return False
        return True

    # Hàm kiểm tra tên tài khoản
    def validate_username(self, username):
        if re.search(r"[^\w\d]", username):
            messagebox.showerror(
                "Error", "Tên tài khoản không được chứa dấu Unicode hoặc dấu cách."
            )
            return False
        return True
        
    def save_users(self):

        with open(self.user_json_path, "w") as file:
            json.dump(self.authorization.user_list, file, indent=4)
        
    # Hàm xóa dữ liệu trong các entry
    def clear_entries(self):
        self.sign_up_username_entry.delete(0, tk.END)
        self.sign_up_password_entry.delete(0, tk.END)
        self.sign_up_confirm_password_entry.delete(0, tk.END)
    
    def show_main_menu_admin(self):
        self.window = tk.Tk()

        self.logo_photo = ImageTk.PhotoImage(LOGO_IMAGE)

        self.window.iconphoto(True, self.logo_photo)
        self.window.title("Quản lý khách hàng")
        self.window.geometry("1920x780+0+0")

        # Frames
        self.top_frame = tk.Frame(self.window, bg="white", height=150)
        self.top_frame.pack(fill=tk.X)

        self.middle_frame = tk.Frame(self.window, bg=BG_BOTTOM_FRAME, height=50)
        self.middle_frame.pack(fill=tk.X)

        self.bottom_frame = tk.Frame(self.window, bg=BG_BOTTOM_FRAME)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Top Frame design
        top_image_path = os.path.join(BASE_DIR, "icon", "customer.png")
        self.top_image = tk.PhotoImage(file=top_image_path)
        self.top_image_label = tk.Label(
            self.top_frame, image=self.top_image, bg="white"
        )
        self.top_image_label.place(anchor="center", relx=0.3, rely=0.5)

        self.top_image2_label = tk.Label(
            self.top_frame, image=self.top_image, bg="white"
        )
        self.top_image2_label.place(anchor="center", relx=0.7, rely=0.5)

        self.heading = tk.Label(
            self.top_frame,
            text="Customers Management System",
            font="arial 20 bold",
            bg="white",
            fg=HEADING_COLOR,
        )
        self.heading.place(anchor="center", relx=0.5, rely=0.5)

        # Middle frame design
        self.middle_role = tk.Label(
            self.middle_frame,
            text=f"Welcome {self.username}\nYour role: {self.role}",
            font="arial 15 bold",
            bg=BG_BOTTOM_FRAME,
            fg=TEXT_COLOR,
        )
        logout_image_path = os.path.join(BASE_DIR, "icon", "logout.png")
        self.logout_image = tk.PhotoImage(file=logout_image_path)

        self.logout_frame = tk.Frame(self.middle_frame, bg=BG_MIDDLE_FRAME)

        self.logout_btn = tk.Button(
            self.logout_frame,
            image=self.logout_image,
            bg=BG_MIDDLE_FRAME,
            command=self.logout,
            bd=3,
            highlightthickness=0,
        )
        self.logout_label = tk.Label(
            self.logout_frame,
            text="Logout",
            font=("Helvetica", 15, "bold"),
            bg=BG_MIDDLE_FRAME,
            fg=TEXT_COLOR,
            padx=10,
        )

        self.logout_label.pack(side="left")
        self.logout_btn.pack(side="left")

        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=1)
        self.middle_frame.grid_columnconfigure(2, weight=1)

        self.middle_role.grid(row=0, column=0, sticky="w", padx=20)
        self.logout_frame.grid(row=0, column=2, sticky="e", padx=20)

        # Buttons
        self.customer_manage_btn = tk.Button(
            self.bottom_frame,
            text="Customer Manager",
            width=30,
            font=("Helvetica", 15, "bold"),
            bg=BTN_COLOR,
            fg=BTN_TEXT_COLOR,
            activebackground=BTN_HOVER_COLOR,
            activeforeground=BTN_TEXT_COLOR,
            command=Functions.customer_manager_window,
            bd=0,
            highlightthickness=0,
        )
        self.user_manage_btn = tk.Button(
            self.bottom_frame,
            text="User Manager",
            width=30,
            font=("Helvetica", 15, "bold"),
            bg=BTN_COLOR,
            fg=BTN_TEXT_COLOR,
            activebackground=BTN_HOVER_COLOR,
            activeforeground=BTN_TEXT_COLOR,
            command=Functions.user_manager_window,
            bd=0,
            highlightthickness=0,
        )

        # Configure grid
        for i in range(NUM_OF_ROW + 1):
            self.bottom_frame.grid_rowconfigure(i, weight=1)
        for j in range(NUM_OF_COLUMN + 2):
            self.bottom_frame.grid_columnconfigure(j, weight=1)

        # Position buttons
        self.customer_manage_btn.grid(row=0, column=1, sticky="ew")
        self.user_manage_btn.grid(row=1, column=1, sticky="ew")

        self.window.mainloop()

    def show_main_menu_user(self):
        self.window = tk.Tk()

        self.logo_photo = ImageTk.PhotoImage(LOGO_IMAGE)

        self.window.title("Quản lý khách hàng")
        self.window.iconphoto(True, self.logo_photo)
        self.window.geometry("1920x780+0+0")

        # Frames
        self.top_frame = tk.Frame(self.window, bg="white", height=150)
        self.top_frame.pack(fill=tk.X)

        self.middle_frame = tk.Frame(self.window, bg=BG_BOTTOM_FRAME, height=50)
        self.middle_frame.pack(fill=tk.X)

        self.bottom_frame = tk.Frame(self.window, bg=BG_BOTTOM_FRAME)
        self.bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Top Frame design
        top_image_path = os.path.join(BASE_DIR, "icon", "customer.png")
        self.top_image = tk.PhotoImage(file=top_image_path)
        self.top_image_label = tk.Label(
            self.top_frame, image=self.top_image, bg="white"
        )
        self.top_image_label.place(anchor="center", relx=0.3, rely=0.5)

        self.top_image2_label = tk.Label(
            self.top_frame, image=self.top_image, bg="white"
        )
        self.top_image2_label.place(anchor="center", relx=0.7, rely=0.5)

        self.heading = tk.Label(
            self.top_frame,
            text="Customers Management System",
            font="arial 20 bold",
            bg="white",
            fg=HEADING_COLOR,
        )
        self.heading.place(anchor="center", relx=0.5, rely=0.5)

        # Middle frame design
        self.middle_role = tk.Label(
            self.middle_frame,
            text=f"Welcome {self.username}\nYour role: {self.role}",
            font="arial 15 bold",
            bg=BG_BOTTOM_FRAME,
            fg=TEXT_COLOR,
        )
        logout_image_path = os.path.join(BASE_DIR, "icon", "logout.png")
        self.logout_image = tk.PhotoImage(file=logout_image_path)

        self.logout_frame = tk.Frame(self.middle_frame, bg=BG_MIDDLE_FRAME)

        self.logout_btn = tk.Button(
            self.logout_frame,
            image=self.logout_image,
            bg=BG_MIDDLE_FRAME,
            command=self.logout,
            bd=3,
            highlightthickness=0,
        )
        self.logout_label = tk.Label(
            self.logout_frame,
            text="Logout",
            font=("Helvetica", 15, "bold"),
            bg=BG_MIDDLE_FRAME,
            fg=TEXT_COLOR,
            padx=10,
        )

        self.logout_label.pack(side="left")
        self.logout_btn.pack(side="left")

        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=1)
        self.middle_frame.grid_columnconfigure(2, weight=1)

        self.middle_role.grid(row=0, column=0, sticky="w", padx=20)
        self.logout_frame.grid(row=0, column=2, sticky="e", padx=20)

        # Buttons
        self.customer_manage_btn = tk.Button(
            self.bottom_frame,
            text="Customer Manager`",
            width=30,
            font=("Helvetica", 15, "bold"),
            bg=BTN_COLOR,
            fg=BTN_TEXT_COLOR,
            activebackground=BTN_HOVER_COLOR,
            activeforeground=BTN_TEXT_COLOR,
            command=Functions.customer_manager_window,
            bd=0,
            highlightthickness=0,
        )

        # Configure grid
        for i in range(NUM_OF_ROW + 1):
            self.bottom_frame.grid_rowconfigure(i, weight=1)
        for j in range(NUM_OF_COLUMN + 2):
            self.bottom_frame.grid_columnconfigure(j, weight=1)

        # Position buttons
        self.customer_manage_btn.grid(row=0, column=1, sticky="ew")

        self.window.mainloop()

    def logout(self):
        self.window.destroy()

        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("400x300+500+200")
        self.create_login_frame()
        self.root.mainloop()
        
    def close_window(self, window):
        window.destroy()


if __name__ == "__main__":
    app = GUI()
