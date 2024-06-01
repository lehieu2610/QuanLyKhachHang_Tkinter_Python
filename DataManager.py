import json

from Customer import Customer


class DataManager:

    # Hàm khởi tạo danh sách và số id để tạo mã id tự động
    def __init__(self):
        self.CustomerList = []

        self.next_id_number = 1

    # Hàm tạo mã tự động
    def generate_customer_id(self):
        while True:
            customer_id = f"MH{self.next_id_number:05d}"
            if not self.findCustomer(customer_id):
                self.next_id_number += 1
                return customer_id
            self.next_id_number += 1

    # Hàm tìm kiếm mã còn trống, nếu không có thì tạo mã mới
    def find_available_id(self):
        for i in range(1, self.next_id_number):
            customer_id = f"MH{i:05d}"
            if not self.findCustomer(customer_id):
                return customer_id
        return self.generate_customer_id()

    # Hàm tìm theo mã và trả về 1 khách hàng
    def findCustomer(self, idToFind):
        for customer in self.CustomerList:
            if customer.id == idToFind:
                return customer
        return False

    # Hàm thêm 1 khách hàng vào danh sách
    def addToList(self, customerToAdd):

        customer_id = self.find_available_id()

        customerToAdd.id = customer_id

        self.CustomerList.append(customerToAdd)

    # Hàm xóa 1 khách hàng khỏi danh sách
    def deleteToList(self, idToDel):

        for customer in self.CustomerList:
            if customer.id == idToDel:
                self.CustomerList.remove(customer)
                return True
        return False

    # Hàm cập nhật 1 khách hàng từ danh sách
    def updateToList(self, id_old_customer, new_customer):

        for customer in self.CustomerList:
            if id_old_customer == customer.id:
                if new_customer.id == id_old_customer:
                    customer.id = new_customer.id
                    customer.name = new_customer.name
                    customer.address = new_customer.address
                    customer.phone_number = new_customer.phone_number
                    customer.email = new_customer.email
                    customer.dob = new_customer.dob
                    return True
                else:
                    for customer in self.CustomerList:
                        if customer.id == new_customer.id:
                            return False
                    customer.id = new_customer.id
                    customer.name = new_customer.name
                    customer.address = new_customer.address
                    customer.phone_number = new_customer.phone_number
                    customer.email = new_customer.email
                    customer.dob = new_customer.dob
                    return True

        return False

    # Hàm đọc dữ liệu từ file json và lưu vào danh sách khách hàng
    def read_data(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            self.CustomerList.clear()
            for customer in data:
                self.CustomerList.append(
                    Customer(
                        customer["id"],
                        customer["name"],
                        customer["address"],
                        customer["phone_number"],
                        customer["email"],
                        customer["dob"],
                    )
                )

    # Hàm viết dữ liệu vào file json
    def write_data(self, file_path):
        data = []

        for customer in self.CustomerList:
            data.append(customer.to_dict())

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    # Hàm lấy ra danh sách khách hàng
    def get_all_customers(self):
        return self.CustomerList

    # Hàm tìm kiếm (danh sách) khách hàng theo mã và tên
    def search_customers(self, search_term):
        return [
            customer
            for customer in self.CustomerList
            if search_term.lower() in customer.id.lower()
            or search_term.lower() in customer.name.lower()
        ]

    """
    Hàm kiểm tra file json người dùng chọn có đúng định dạng chưa
    Mô tả: 1 file json đúng định dạng là data chứa ở dạng list và mỗi dict trong data đều phải có thuộc tính: 
    id, name, address, phone_number, email, dob
    """

    @staticmethod
    def is_valid_json(file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read().strip()
                if not content:
                    return True
                data = json.loads(content)
                if isinstance(data, list):
                    for customer in data:
                        if not all(
                            key in customer
                            for key in (
                                "id",
                                "name",
                                "address",
                                "phone_number",
                                "email",
                                "dob",
                            )
                        ):
                            return False
                    return True
                return False
        except (json.JSONDecodeError, IOError, FileNotFoundError):
            return False
