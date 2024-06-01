import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
from datetime import datetime
from tkinter import filedialog
import requests
import os
from PIL import Image, ImageTk

from Customer import Customer
from DataManager import DataManager

BASE_DIR = os.path.dirname(__file__)
LOGO_PATH = os.path.join(BASE_DIR, "icon", "logo.png")
LOGO_IMAGE = Image.open(LOGO_PATH)


class Application:
    # Hàm khởi tạo giao diện
    def __init__(self, window):
        self.window = window
        self.dataManager = DataManager()

        self.flag_save = True 

        self.file_path = False

        self.logo_photo = ImageTk.PhotoImage(LOGO_IMAGE)

        self.window.title("Quản lý khách hàng")
        self.window.iconphoto(True, self.logo_photo)
        self.window.geometry("1920x780+0+0")

        # INFO FRAMES

        infoFrame = tk.Frame(self.window, height=100, width=1980, bg="green")
        infoFrame.pack(side="top", fill=tk.X)

        # FUNCTIONS FRAME
        self.functions_frame = tk.Frame(self.window, height=700, width=560)
        self.functions_frame.place(relx=0.62, rely=0.55, anchor="w")

        # ADD FRAME
        self.add_frame = tk.Frame(self.functions_frame, height=700 / 3, width=560)
        self.add_frame.place(relx=0.95, rely=0.12, anchor="e")
        self.create_add_frame()

        # DELETE FRAME
        self.delete_frame = tk.Frame(self.functions_frame, height=700 / 3, width=560)
        self.delete_frame.place(relx=1, rely=0.43, anchor="e")
        self.create_delete_frame()

        # UPDATE FRAME
        self.update_frame = tk.Frame(self.functions_frame, height=700 / 3, width=560)
        self.update_frame.place(relx=1, rely=0.76, anchor="e")
        self.create_update_frame()

        # BUTTONS

        self.new_file_btn = tk.Button(
            infoFrame,
            text="Tạo file mới",
            width=10,
            command=self.create_new_file,
            padx=2,
            pady=2,
        )
        self.select_file_btn = tk.Button(
            infoFrame,
            text="Mở file",
            width=10,
            command=self.open_file_dialog,
            padx=2,
            pady=2,
        )
        self.save_file_btn = tk.Button(
            infoFrame, text="Lưu", width=10, command=self.save, padx=2, pady=2
        )
        self.exit_btn = tk.Button(
            infoFrame,
            text="Thoát",
            width=10,
            command=lambda: self.close_window(self.window),
            padx=2,
            pady=2,
        )

        for i in range(20):
            infoFrame.grid_columnconfigure(i, weight=1)

        self.new_file_btn.grid(row=0, column=6, padx=5, sticky="nsew", pady=5)
        self.select_file_btn.grid(row=0, column=8, padx=5, sticky="nsew", pady=5)
        self.save_file_btn.grid(row=0, column=10, padx=5, sticky="nsew", pady=5)
        self.exit_btn.grid(row=0, column=12, padx=5, sticky="nsew", pady=5)

        self.show_data_table(self.window)

        self.window.mainloop()

    # Frame của phần thêm khách hàng
    def create_add_frame(self):
        label_frame = tk.LabelFrame(
            self.add_frame, text="Thêm khách hàng", font=("Arial", 14)
        )
        label_frame.pack(fill="both", expand=True, padx=10, pady=10)

        nameLabel = tk.Label(label_frame, text="Họ tên: ")
        nameLabel.grid(row=0, column=0, sticky="e", pady=5)
        self.name_add_entry = tk.Entry(label_frame, width=20, font=("Arial", 12))
        self.name_add_entry.grid(row=0, column=1, pady=5)

        addressLabel = tk.Label(label_frame, text="Địa chỉ: ")
        addressLabel.grid(row=1, column=0, sticky="e", pady=5)
        self.address_add_entry = tk.Entry(label_frame, width=20, font=("Arial", 12))
        self.address_add_entry.grid(row=1, column=1, pady=5)

        phoneLabel = tk.Label(label_frame, text="Số điện thoại: ")
        phoneLabel.grid(row=0, column=2, sticky="e", pady=5)
        self.phone_add_entry = tk.Entry(label_frame, width=20, font=("Arial", 12))
        self.phone_add_entry.grid(row=0, column=3, pady=5)

        emailLabel = tk.Label(label_frame, text="Email: ")
        emailLabel.grid(row=1, column=2, sticky="e", pady=5)
        self.email_add_entry = tk.Entry(label_frame, width=20, font=("Arial", 12))
        self.email_add_entry.grid(row=1, column=3, pady=5)

        dobLabel = tk.Label(label_frame, text="Ngày sinh: ")
        dobLabel.grid(row=2, column=0, sticky="e", pady=5)
        self.dob_add_entry = tk.Entry(label_frame, width=20, font=("Arial", 12))
        self.dob_add_entry.grid(row=2, column=1, pady=5)

        self.add_btn = tk.Button(
            label_frame, text="Thêm", width=20, command=self.add_customer
        )
        self.add_btn.grid(row=3, column=1, columnspan=1, pady=(10, 0))

        self.add_api_btn = tk.Button(
            label_frame,
            text="Thêm bằng lấy API",
            width=20,
            command=self.submit_api_window,
        )
        self.add_api_btn.grid(row=3, column=2, columnspan=3, pady=(10, 0))

    # Frame của phần xóa khách hàng
    def create_delete_frame(self):
        label_frame = tk.LabelFrame(
            self.delete_frame, text="Xóa khách hàng", font=("Arial", 14)
        )
        label_frame.pack(fill="both", expand=True, padx=10, pady=10)

        id_find_label = tk.Label(label_frame, text="Mã khách hàng: ")
        id_find_label.grid(row=0, column=0, sticky="e", pady=5)
        self.id_find_delete_entry = tk.Entry(label_frame, width=20, font=("Arial", 12))
        self.id_find_delete_entry.grid(row=0, column=1, pady=5)

        findBtn = tk.Button(
            label_frame,
            text="Hiển thị",
            height=1,
            width=10,
            command=lambda: self.find_customer(
                self.id_delete_entry,
                self.name_delete_entry,
                self.address_delete_entry,
                self.phone_delete_entry,
                self.email_delete_entry,
                self.dob_delete_entry,
                self.id_find_delete_entry,
                "delete",
            ),
            bd=3,
        )
        findBtn.grid(row=1, column=1, padx=40)

        id_delete_label = tk.Label(label_frame, text="Mã khách hàng: ")
        id_delete_label.grid(row=2, column=0, sticky="e", pady=5)
        self.id_delete_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.id_delete_entry.grid(row=2, column=1, pady=5)

        nameLabel = tk.Label(label_frame, text="Họ tên: ")
        nameLabel.grid(row=3, column=0, sticky="e", pady=5)
        self.name_delete_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.name_delete_entry.grid(row=3, column=1, pady=5)

        addressLabel = tk.Label(label_frame, text="Địa chỉ: ")
        addressLabel.grid(row=4, column=0, sticky="e", pady=5)
        self.address_delete_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.address_delete_entry.grid(row=4, column=1, pady=5)

        phoneLabel = tk.Label(label_frame, text="Số điện thoại: ")
        phoneLabel.grid(row=2, column=2, sticky="e", pady=5)
        self.phone_delete_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.phone_delete_entry.grid(row=2, column=3, pady=5)

        emailLabel = tk.Label(label_frame, text="Email: ")
        emailLabel.grid(row=3, column=2, sticky="e", pady=5)
        self.email_delete_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.email_delete_entry.grid(row=3, column=3, pady=5)

        dobLabel = tk.Label(label_frame, text="Ngày sinh: ")
        dobLabel.grid(row=4, column=2, sticky="e", pady=5)
        self.dob_delete_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.dob_delete_entry.grid(row=4, column=3, pady=5)

        self.delete_btn = tk.Button(
            label_frame, text="Xóa", width=20, command=self.delete_customer
        )
        self.delete_btn.grid(row=5, column=1, columnspan=1, pady=(10, 0), padx=10)
        
        self.delete_all_btn = tk.Button(
            label_frame, text="Xóa tất cả", width=20, command=self.delete_all
        )
        self.delete_all_btn.grid(row=5, column=2, columnspan=3, pady=(10, 0), padx=10)

    # Frame của phần sửa khách hàng
    def create_update_frame(self):
        label_frame = tk.LabelFrame(
            self.update_frame, text="Cập nhật khách hàng", font=("Arial", 14)
        )
        label_frame.pack(fill="both", expand=True, padx=10, pady=10)

        id_find_label = tk.Label(label_frame, text="Mã khách hàng: ")
        id_find_label.grid(row=0, column=0, sticky="e", pady=5)
        self.id_find_update_entry = tk.Entry(label_frame, width=20, font=("Arial", 12))
        self.id_find_update_entry.grid(row=0, column=1, pady=5)

        findBtn = tk.Button(
            label_frame,
            text="Tìm kiếm",
            height=1,
            width=10,
            command=lambda: self.find_customer(
                self.id_update_entry,
                self.name_update_entry,
                self.address_update_entry,
                self.phone_update_entry,
                self.email_update_entry,
                self.dob_update_entry,
                self.id_find_update_entry,
                "update",
            ),
            bd=3,
        )
        findBtn.grid(row=1, column=1, padx=40)

        id_update_label = tk.Label(label_frame, text="Mã khách hàng: ")
        id_update_label.grid(row=2, column=0, sticky="e", pady=5)
        self.id_update_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.id_update_entry.grid(row=2, column=1, pady=5)

        nameLabel = tk.Label(label_frame, text="Họ tên: ")
        nameLabel.grid(row=3, column=0, sticky="e", pady=5)
        self.name_update_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.name_update_entry.grid(row=3, column=1, pady=5)

        addressLabel = tk.Label(label_frame, text="Địa chỉ: ")
        addressLabel.grid(row=4, column=0, sticky="e", pady=5)
        self.address_update_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.address_update_entry.grid(row=4, column=1, pady=5)

        phoneLabel = tk.Label(label_frame, text="Số điện thoại: ")
        phoneLabel.grid(row=2, column=2, sticky="e", pady=5)
        self.phone_update_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.phone_update_entry.grid(row=2, column=3, pady=5)

        emailLabel = tk.Label(label_frame, text="Email: ")
        emailLabel.grid(row=3, column=2, sticky="e", pady=5)
        self.email_update_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.email_update_entry.grid(row=3, column=3, pady=5)
        dobLabel = tk.Label(label_frame, text="Ngày sinh: ")
        dobLabel.grid(row=4, column=2, sticky="e", pady=5)
        self.dob_update_entry = tk.Entry(
            label_frame, width=20, font=("Arial", 12), state="disabled"
        )
        self.dob_update_entry.grid(row=4, column=3, pady=5)

        self.update_btn = tk.Button(
            label_frame, text="Cập nhật", width=20, command=self.update_customer
        )
        self.update_btn.grid(row=5, column=1, columnspan=3, pady=(10, 0))

    # Hàm xóa dữ liệu entry của 3 frame thêm, xóa, sửa
    def clear_add_frame(self):
        self.name_add_entry.delete(0, tk.END)
        self.address_add_entry.delete(0, tk.END)
        self.phone_add_entry.delete(0, tk.END)
        self.email_add_entry.delete(0, tk.END)
        self.dob_add_entry.delete(0, tk.END)

    def clear_delete_frame(self):
        self.id_delete_entry.config(state=tk.NORMAL)
        self.name_delete_entry.config(state=tk.NORMAL)
        self.address_delete_entry.config(state=tk.NORMAL)
        self.phone_delete_entry.config(state=tk.NORMAL)
        self.email_delete_entry.config(state=tk.NORMAL)
        self.dob_delete_entry.config(state=tk.NORMAL)
        self.id_find_delete_entry.config(state=tk.NORMAL)

        self.id_delete_entry.delete(0, tk.END)
        self.name_delete_entry.delete(0, tk.END)
        self.address_delete_entry.delete(0, tk.END)
        self.phone_delete_entry.delete(0, tk.END)
        self.email_delete_entry.delete(0, tk.END)
        self.dob_delete_entry.delete(0, tk.END)
        self.id_find_delete_entry.delete(0, tk.END)

        self.id_delete_entry.config(state=tk.DISABLED)
        self.name_delete_entry.config(state=tk.DISABLED)
        self.address_delete_entry.config(state=tk.DISABLED)
        self.phone_delete_entry.config(state=tk.DISABLED)
        self.email_delete_entry.config(state=tk.DISABLED)
        self.dob_delete_entry.config(state=tk.DISABLED)

    def clear_update_frame(self):

        self.id_update_entry.config(state=tk.NORMAL)
        self.name_update_entry.config(state=tk.NORMAL)
        self.address_update_entry.config(state=tk.NORMAL)
        self.phone_update_entry.config(state=tk.NORMAL)
        self.email_update_entry.config(state=tk.NORMAL)
        self.dob_update_entry.config(state=tk.NORMAL)
        self.id_find_update_entry.config(state=tk.NORMAL)

        self.id_update_entry.delete(0, tk.END)
        self.name_update_entry.delete(0, tk.END)
        self.address_update_entry.delete(0, tk.END)
        self.phone_update_entry.delete(0, tk.END)
        self.email_update_entry.delete(0, tk.END)
        self.dob_update_entry.delete(0, tk.END)
        self.id_find_update_entry.delete(0, tk.END)

        self.id_update_entry.config(state=tk.DISABLED)
        self.name_update_entry.config(state=tk.DISABLED)
        self.address_update_entry.config(state=tk.DISABLED)
        self.phone_update_entry.config(state=tk.DISABLED)
        self.email_update_entry.config(state=tk.DISABLED)
        self.dob_update_entry.config(state=tk.DISABLED)

    # Hàm tạo bảng TreeView
    def show_data_table(self, window):
        listFrame = tk.Frame(window)
        listFrame.place(relx=0.61, rely=0.51, anchor="e", height=700)

        find_frame = tk.Frame(listFrame)
        find_frame.pack(side="top", fill="x")

        self.find_customer_entry = tk.Entry(find_frame, width=50)
        self.find_customer_entry.pack(side="left", padx=10, pady=10)

        self.find_customer_btn = tk.Button(
            find_frame, text="Tìm khách hàng", command=self.find_customer_by_id_name
        )
        self.find_customer_btn.pack(side="left", padx=10, pady=10)

        sort_frame = tk.Frame(find_frame)
        sort_frame.pack(side="right", padx=10, pady=10)

        self.sort_combobox = ttk.Combobox(
            sort_frame, values=["Mã khách hàng", "Họ tên", "Ngày sinh"]
        )
        self.sort_combobox.set("Sắp xếp theo")
        self.sort_combobox.pack(side="left", padx=10, pady=10)
        self.sort_combobox.bind("<<ComboboxSelected>>", self.sort_data)

        self.order_combobox = ttk.Combobox(sort_frame, values=["Tăng dần", "Giảm dần"])
        self.order_combobox.set("Thứ tự")
        self.order_combobox.pack(side="left", padx=10, pady=10)
        self.order_combobox.bind("<<ComboboxSelected>>", self.sort_data)

        headers = (
            "Mã khách hàng",
            "Họ tên",
            "Địa chỉ",
            "SĐT",
            "Email",
            "Ngày sinh",
        )
        self.dataTable = ttk.Treeview(listFrame, columns=headers, show="headings")

        yscroll = ttk.Scrollbar(listFrame, orient="vertical")
        yscroll.pack(side="right", fill="y")

        xscroll = ttk.Scrollbar(listFrame, orient="horizontal")
        xscroll.pack(side="bottom", fill="x")

        self.dataTable.configure(xscrollcommand=xscroll.set)
        self.dataTable.configure(yscrollcommand=yscroll.set)

        xscroll.config(command=self.dataTable.yview)
        xscroll.config(command=self.dataTable.xview)

        for col in headers:
            self.dataTable.heading(col, text=col, anchor="w")
            self.dataTable.column(col, width=150, stretch=False)
        self.dataTable.pack(fill="both", expand=True)

    # Hàm tìm (danh sách) khách hàng theo mã và tên
    def find_customer_by_id_name(self):
        search_term = self.find_customer_entry.get()
        if not search_term:
            self.update_data_table()
            return

        for item in self.dataTable.get_children():
            self.dataTable.delete(item)

        customers = self.dataManager.search_customers(search_term)

        if not customers:
            messagebox.showinfo("Thông báo", "Không tìm thấy khách hàng")
            return

        for customer in customers:
            self.dataTable.insert(
                "",
                "end",
                values=(
                    customer.id,
                    customer.name,
                    customer.address,
                    customer.phone_number,
                    customer.email,
                    customer.dob,
                ),
            )

    # Hàm sắp xếp dữ liệu
    def sort_data(self, event):
        sort_by = self.sort_combobox.get()
        order = self.order_combobox.get()
        customers = self.dataManager.get_all_customers()

        if sort_by == "Mã khách hàng":
            key_func = lambda x: x.id
        elif sort_by == "Họ tên":
            key_func = lambda x: x.name
        elif sort_by == "Ngày sinh":
            key_func = lambda x: x.get_age()
        else:
            return

        reverse = order == "Giảm dần"
        customers.sort(key=key_func, reverse=reverse)

        for item in self.dataTable.get_children():
            self.dataTable.delete(item)

        for customer in customers:
            self.dataTable.insert(
                "",
                "end",
                values=(
                    customer.id,
                    customer.name,
                    customer.address,
                    customer.phone_number,
                    customer.email,
                    customer.dob,
                ),
            )

    # Các hàm kiểm tra tính đúng đắn của dữ liệu nhập vào
    def is_full_filled(
        self, id_entry, name_entry, address_entry, phone_entry, email_entry, dob_entry
    ):
        id = id_entry.get()
        name = name_entry.get()
        address = address_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        dob = dob_entry.get()

        if id and name and address and phone and email and dob:
            return Customer(id, name, address, phone, email, dob)
        else:
            return False

    def is_correct_email(self, email_entry):
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

        if re.match(pattern, email_entry.get()) == None:
            return False
        else:
            return True

    def is_correct_dob(self, dob_entry):
        pattern = r"\b[0-9]{1,2}/[0-9]{1,2}/[0-9]{1,4}"

        if re.match(pattern, dob_entry.get()):
            try:
                date_obj = datetime.strptime(dob_entry.get(), "%d/%m/%Y")

                if datetime.now() < date_obj:
                    return False

                return True
            except ValueError:
                return False

        return False

    def is_correct_filled(
        self, id_entry, name_entry, address_entry, phone_entry, email_entry, dob_entry
    ):

        if (
            self.is_full_filled(
                id_entry, name_entry, address_entry, phone_entry, email_entry, dob_entry
            )
            == False
        ):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return False
        elif self.is_correct_email(email_entry) == False:
            messagebox.showwarning("Cảnh báo", "Email chưa đúng định dạng")
            return False
        elif self.is_correct_dob(dob_entry) == False:
            messagebox.showwarning("Cảnh báo", "Ngày sinh không hợp lệ")
            return False
        else:
            id = id_entry.get()
            name = name_entry.get()
            address = address_entry.get()
            phone = phone_entry.get()
            email = email_entry.get()
            dob = dob_entry.get()
            return Customer(id, name, address, phone, email, dob)

    # Hàm thêm khách hàng
    def add_customer(self):

        customer_to_add = self.is_correct_filled(
            self.name_add_entry,
            self.name_add_entry,
            self.address_add_entry,
            self.phone_add_entry,
            self.email_add_entry,
            self.dob_add_entry,
        )
        if customer_to_add == False:
            return
        else:
            self.dataManager.addToList(customer_to_add)
            self.dataTable.insert(
                "",
                "end",
                values=(
                    customer_to_add.id,
                    customer_to_add.name,
                    customer_to_add.address,
                    customer_to_add.phone_number,
                    customer_to_add.email,
                    customer_to_add.dob,
                ),
            )
            self.flag_save = False
            messagebox.showinfo("Thông báo", "Thêm thành công")
            self.clear_add_frame()

    # Giao diện gửi link API
    def submit_api_window(self):
        self.api_window = tk.Toplevel(self.window)
        self.api_window.title("Nhập Link API")
        self.api_window.geometry("400x200")

        self.api_label = tk.Label(self.api_window, text="Link API:")
        self.api_label.pack(pady=10)

        self.api_entry = tk.Entry(self.api_window, width=50)
        self.api_entry.pack(pady=10)

        self.submit_button = tk.Button(
            self.api_window, text="Submit", command=self.add_customer_get_API
        )
        self.submit_button.pack(pady=10)

    # Hàm thêm (danh sách) khách hàng vào danh sách hiện tại bằng GET API
    def add_customer_get_API(self):

        api_url = self.api_entry.get()
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json().get("data", [])

            for customer_data in data:

                new_customer = Customer(
                    "",
                    customer_data["name"],
                    customer_data["address"],
                    customer_data["phone"],
                    customer_data["email"],
                    customer_data["dob"],
                )

                self.dataManager.addToList(new_customer)
                self.flag_save = False

            self.update_data_table()
            messagebox.showinfo("Thông báo", "Thêm khách hàng từ API thành công")
            self.api_window.destroy()
        except requests.RequestException as e:
            messagebox.showerror("Lỗi", f"Không thể lấy dữ liệu từ API: {e}")
        except ValueError:
            messagebox.showerror("Lỗi", "Dữ liệu từ API không hợp lệ")

    # Hàm xóa khách hàng
    def delete_customer(self):

        idToDel = self.id_find_delete_entry.get()

        if idToDel == "":
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return

        choice = messagebox.askyesno(
            "Thông báo", "Bạn chắc chắn muốn xóa khách hàng này?"
        )

        if choice:

            if self.dataManager.deleteToList(idToDel):
                for customer in self.dataTable.get_children():
                    if self.dataTable.item(customer, "values")[0] == idToDel:
                        self.dataTable.delete(customer)
                        break
                self.flag_save = False
                messagebox.showinfo("Thông báo", "Xóa thành công")
                self.clear_delete_frame()
                return
            else:
                messagebox.showerror("Error", "Mã khách hàng không tồn tại")
                return
        else:
            self.clear_delete_frame()
            return

    def delete_all(self):
        
        if len(self.dataManager.CustomerList) == 0:
            messagebox.showerror("Lỗi","Danh sách khách hàng rỗng")
        
        else:
            
            choice = messagebox.askyesno("Thông báo","Bạn chắc chắn muốn xóa tất cả khách hàng?")
            
            if choice:
                
                self.dataManager.CustomerList.clear()
                
                self.clear_data_table()
                
                self.flag_save = False
                
                messagebox.showinfo("Thông báp", "Đã xóa tất cả khách hàng")
                
                return
            else:
                return
            
    # Hàm cập nhật khách hàng
    def update_customer(self):

        customer_to_update = self.is_correct_filled(
            self.id_update_entry,
            self.name_update_entry,
            self.address_update_entry,
            self.phone_update_entry,
            self.email_update_entry,
            self.dob_update_entry,
        )

        if customer_to_update == False:
            return

        choice = messagebox.askyesno("Thông báo", "Bạn muốn cập nhật khách hàng này?")

        if choice:

            if self.dataManager.updateToList(
                self.id_find_update_entry.get(), customer_to_update
            ):

                for item in self.dataTable.get_children():
                    customer = self.dataTable.item(item, "values")
                    if customer[0] == self.id_find_update_entry.get():
                        self.dataTable.item(
                            item,
                            values=(
                                customer_to_update.id,
                                customer_to_update.name,
                                customer_to_update.address,
                                customer_to_update.phone_number,
                                customer_to_update.email,
                                customer_to_update.dob,
                            ),
                        )
                        break

                self.id_update_entry.config(state=tk.DISABLED)
                self.name_update_entry.config(state=tk.DISABLED)
                self.address_update_entry.config(state=tk.DISABLED)
                self.phone_update_entry.config(state=tk.DISABLED)
                self.email_update_entry.config(state=tk.DISABLED)
                self.dob_update_entry.config(state=tk.DISABLED)
                messagebox.showinfo("Thông báo", "Cập nhật thành công")
                self.flag_save = False
                self.clear_update_frame()
            else:
                messagebox.showerror("Lỗi", "Mã khách hàng đã tồn tại")
        else:
            self.clear_update_frame()
            return

    # Hàm lưu file
    def save(self):

        if self.file_path:

            self.dataManager.write_data(self.file_path)
            messagebox.showinfo(title="Quản lý khách hàng", message="Lưu thành công")
            self.flag_save = True

        else:
            self.file_path = filedialog.asksaveasfilename(
                defaultextension=".json", filetypes=[("JSON files", "*.json")]
            )
            self.dataManager.write_data(self.file_path)
            messagebox.showinfo(title="Quản lý khách hàng", message="Lưu thành công")
            self.flag_save = True

    # Hàm tải dữ liệu lên bảng TreeView và danh sách khách hàng
    def upload(self):

        for item in self.dataTable.get_children():
            self.dataTable.delete(item)

        self.dataManager.read_data(self.file_path)

        for customer in self.dataManager.CustomerList:
            self.dataTable.insert(
                "",
                "end",
                values=(
                    customer.id,
                    customer.name,
                    customer.address,
                    customer.phone_number,
                    customer.email,
                    customer.dob,
                ),
            )

    # Hàm cập nhật lại dữ liệu cho bảng TreeView
    def update_data_table(self):

        self.clear_data_table()

        for customer in self.dataManager.CustomerList:
            self.dataTable.insert(
                "",
                "end",
                values=(
                    customer.id,
                    customer.name,
                    customer.address,
                    customer.phone_number,
                    customer.email,
                    customer.dob,
                ),
            )

    # Hàm xóa toàn bộ dữ liệu cho bảng TreeView
    def clear_data_table(self):
        for item in self.dataTable.get_children():
            self.dataTable.delete(item)

    # Hàm đóng cửa sổ
    def close_window(self, window):
        if self.flag_save:
            window.destroy()
        else:
            choice = messagebox.askyesnocancel(
                "Cảnh báo", "Bạn vẫn chưa lưu file, bạn muốn lưu chứ?"
            )
            if choice == True:
                self.save()
                window.destroy()
            elif choice == False:
                window.destroy()
            else:
                return

    # Hàm để lựa chọn file json từ máy tính
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(
            title="Chọn tệp JSON",
            filetypes=[("JSON files", "*.json")],
            initialdir=".",
        )
        if self.dataManager.is_valid_json(file_path):
            self.file_path = file_path
            self.upload()
        else:
            messagebox.showerror("Loi", "File json khong dung dinh dang")

    # Hàm tạo 1 file json mới để thao tác
    def create_new_file(self):

        if self.file_path != False:
            choice = messagebox.askyesnocancel(
                "Thông báo", "Bạn có muốn lưu file hiện tại không?"
            )

            if choice:
                self.save()
                self.clear_data_table()
                self.dataManager.CustomerList.clear()
                messagebox.showinfo("Thông báo", "Tạo file mới thành công")

            else:
                self.clear_data_table()
                self.dataManager.CustomerList.clear()
                messagebox.showinfo("Thông báo", "Tạo file mới thành công")

            self.file_path = False

        else:
            self.clear_data_table()
            self.dataManager.CustomerList.clear()
            messagebox.showinfo("Thông báo", "Tạo file mới thành công")

    # Hàm tìm khách hàng bằng id và hiển thị thông tin ra các entry
    def find_customer(
        self,
        id_entry,
        name_entry,
        address_entry,
        phone_entry,
        email_entry,
        dob_entry,
        find_entry,
        function_type,
    ):

        id_entry.config(state=tk.NORMAL)
        name_entry.config(state=tk.NORMAL)
        address_entry.config(state=tk.NORMAL)
        phone_entry.config(state=tk.NORMAL)
        email_entry.config(state=tk.NORMAL)
        dob_entry.config(state=tk.NORMAL)

        id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        dob_entry.delete(0, tk.END)

        id_entry.config(state=tk.DISABLED)
        name_entry.config(state=tk.DISABLED)
        address_entry.config(state=tk.DISABLED)
        phone_entry.config(state=tk.DISABLED)
        email_entry.config(state=tk.DISABLED)
        dob_entry.config(state=tk.DISABLED)

        for customer in self.dataManager.CustomerList:
            if find_entry.get() == customer.id:

                id_entry.config(state=tk.NORMAL)
                name_entry.config(state=tk.NORMAL)
                address_entry.config(state=tk.NORMAL)
                phone_entry.config(state=tk.NORMAL)
                email_entry.config(state=tk.NORMAL)
                dob_entry.config(state=tk.NORMAL)

                id_entry.insert(tk.END, customer.id)
                name_entry.insert(tk.END, customer.name)
                address_entry.insert(tk.END, customer.address)
                phone_entry.insert(tk.END, customer.phone_number)
                email_entry.insert(tk.END, customer.email)
                dob_entry.insert(tk.END, customer.dob)

                if function_type == "delete":
                    id_entry.config(state=tk.DISABLED)
                    name_entry.config(state=tk.DISABLED)
                    address_entry.config(state=tk.DISABLED)
                    phone_entry.config(state=tk.DISABLED)
                    email_entry.config(state=tk.DISABLED)
                    dob_entry.config(state=tk.DISABLED)
                    return
                else:
                    return
        messagebox.showerror(title="Lỗi", message="Không tìm thấy khách hàng")


def main():

    window = tk.Tk()
    window.title("Quản lý khách hàng")
    window.geometry("1920x780+0+0")
    app = Application(window)


if __name__ == "__main__":
    main()
