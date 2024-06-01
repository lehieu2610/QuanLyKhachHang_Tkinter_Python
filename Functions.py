import sys
from subprocess import call
import os

BASE_DIR = os.path.dirname(__file__)

class Functions:
    @staticmethod
    def customer_manager_window():
        call([sys.executable, os.path.join(BASE_DIR, "CustomerManager.py")])

    @staticmethod
    def user_manager_window():
        call([sys.executable, os.path.join(BASE_DIR, "UserManager.py")])
