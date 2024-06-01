import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import json
import os
from PIL import Image, ImageTk

from Authorization import Authorization

BASE_DIR = os.path.dirname(__file__)
LOGO_PATH = os.path.join(BASE_DIR, "icon", "logo.png")
LOGO_IMAGE = Image.open(LOGO_PATH)


class Application:
    def __init__(self, window):
        self.window = window
        self.authorization = Authorization()

        self.logo_photo = ImageTk.PhotoImage(LOGO_IMAGE)

        self.window.title("Quản trị người dùng")
        self.window.iconphoto(True, self.logo_photo)
        self.window.geometry("800x600")
        self.window.config(bg="white")

        self.user_json_path = os.path.join(BASE_DIR, "user.json")


        # Kiểm tra xem tệp user.json đã tồn tại chưa
        if not os.path.exists(self.user_json_path):
            # Nếu không tồn tại, tạo tệp user.json
            with open(self.user_json_path, "w") as file:
                json.dump([], file)

        self.info_frame = tk.Frame(self.window, bg="cyan")
        self.info_frame.pack(side="top", fill=tk.BOTH)

        self.title_label = tk.Label(
            self.info_frame, text="User Manager", font="arial 20 bold", bg="cyan"
        )
        self.title_label.pack(pady=10)

        self.create_widgets()
        self.populate_treeview()

    # Hàm lưu danh sách người dùng vào tệp user.json
    def save_users(self):

        with open(self.user_json_path, "w") as file:
            json.dump(self.authorization.user_list, file, indent=4)

    # Hàm tạo tất cả các widget trong giao diện
    def create_widgets(self):

        self.frame = tk.Frame(self.window, bg="white", width=300, height=300)
        self.frame.pack(pady=10)

        self.username_label = tk.Label(self.frame, text="Tên tài khoản:", bg="white")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.frame, text="Mật khẩu:", bg="white")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.confirm_password_label = tk.Label(
            self.frame, text="Nhập lại mật khẩu:", bg="white"
        )
        self.confirm_password_label.grid(row=2, column=0, padx=5, pady=5)
        self.confirm_password_entry = tk.Entry(self.frame, show="*")
        self.confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.role_label = tk.Label(self.frame, text="Vai trò:", bg="white")
        self.role_label.grid(row=3, column=0, padx=5, pady=5)
        self.role_var = tk.StringVar()
        self.role_var.set("user")
        self.user_radio = tk.Radiobutton(
            self.frame, text="User", variable=self.role_var, value="user", bg="white"
        )
        self.user_radio.grid(row=3, column=1, padx=5, pady=5)
        self.admin_radio = tk.Radiobutton(
            self.frame, text="Admin", variable=self.role_var, value="admin", bg="white"
        )
        self.admin_radio.grid(row=3, column=2, padx=5, pady=5)

        # BUTTONS
        self.create_button = tk.Button(
            self.frame, text="Tạo mới", command=self.create_user, width=10
        )
        self.create_button.grid(row=4, column=0, padx=5, pady=5)

        self.update_button = tk.Button(
            self.frame, text="Sửa", command=self.update_user, width=10
        )
        self.update_button.grid(row=4, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(
            self.frame, text="Xóa", command=self.delete_user, width=10
        )
        self.delete_button.grid(row=4, column=2, padx=5, pady=5)

        self.exit_button = tk.Button(
            self.frame, text="Thoát", command=self.close_window, width=10
        )
        self.exit_button.grid(row=5, column=1, padx=5, pady=5)

        self.tree = ttk.Treeview(
            self.window, columns=("username", "password", "role"), show="headings"
        )
        self.tree.heading("username", text="Tên tài khoản")
        self.tree.heading("password", text="Mật khẩu")
        self.tree.heading("role", text="Vai trò")
        self.tree.pack(pady=20, padx=10, fill=tk.BOTH, expand=True)

    # Hàm add dữ liệu vào bảng người dùng TreeView
    def populate_treeview(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for user in self.authorization.user_list:
            self.tree.insert(
                "", "end", values=(user["username"], user["password"], user["role"])
            )

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

    def is_exist_username(self, username):
        
        for account in self.authorization.user_list:
            if username == account["username"]:
                return True
        return False
        

    # Hàm thêm 1 user
    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
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
            "role": self.role_var.get(),
        }
        self.authorization.user_list.append(new_user)
        self.save_users()
        self.populate_treeview()
        messagebox.showinfo("Success", "Tạo tài khoản thành công!")
        self.clear_entries()

    # Hàm cập nhật 1 user
    def update_user(self):
        username = self.username_entry.get()
        new_password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not username or not new_password:
            messagebox.showerror(
                "Error", "Vui lòng nhập tên tài khoản và mật khẩu mới."
            )
            return

        if not self.validate_password(new_password, confirm_password):
            return

        for user in self.authorization.user_list:
            if user["username"] == username:
                user["password"] = new_password
                self.save_users()
                self.populate_treeview()
                messagebox.showinfo("Success", "Cập nhật tài khoản thành công!")
                self.clear_entries()
                return
        messagebox.showerror("Error", "Tài khoản không tồn tại.")

    # Hàm xóa 1 user
    def delete_user(self):
        username = self.username_entry.get()

        if not username:
            messagebox.showerror("Error", "Vui lòng nhập tên tài khoản.")
            return

        for user in self.authorization.user_list:
            if user["username"] == username:
                self.authorization.user_list.remove(user)
                self.save_users()
                self.populate_treeview()
                messagebox.showinfo("Success", "Xóa tài khoản thành công!")
                self.clear_entries()
                return

        messagebox.showerror("Error", "Tài khoản không tồn tại.")

    # Hàm xóa dữ liệu trong các entry
    def clear_entries(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)

    def close_window(self):
        self.window.destroy()


def main():
    window = tk.Tk()
    app = Application(window)
    window.mainloop()


if __name__ == "__main__":
    main()
