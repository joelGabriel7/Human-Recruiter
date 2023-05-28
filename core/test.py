from config.wsgi import *
import random
import string
from datetime import date
from django.utils import timezone


# from core.erp.models import *


def generate_employee_code():
    letters = string.ascii_uppercase
    numbers = string.digits
    code = ''.join(random.choice(letters)
                   for i in range(6)) + ''.join(random.choice(numbers) for i in range(3))
    return code


print(generate_employee_code())
