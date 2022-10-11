from typing import Iterable

from prettytable import PrettyTable



class Employee:

    user_editable_attributes = ['title', 'forename', 'surname', 'email', 'salary']

    def __init__(self):
        self.id = 0
        self.title = ''
        self.forename = ''
        self.surname = ''
        self.email = ''
        self.salary = 0.0

    @staticmethod
    def from_user_input(existing_data = None):
        e = Employee()

        for attribute in e.user_editable_attributes:
            setattr(e, attribute, input(f"{attribute.capitalize()}:\t"))

        return e

    @staticmethod
    def from_db_result(result_tuple):
        try:
            e = Employee()
            e.set_employee_id(result_tuple[0])
            e.set_employee_title(result_tuple[1])
            e.set_forename(result_tuple[2])
            e.set_surname(result_tuple[3])
            e.set_email(result_tuple[4])
            e.set_salary(result_tuple[5])
            return e
        except TypeError:
            return None

    def apply_user_update(self):
        print ("Enter updated attributes. Leave blank to accept current value")
        for attribute in self.user_editable_attributes:
            current_value = getattr(self,attribute)
            user_input = input(f'{attribute.capitalize()} [{current_value}]:\t')
            if user_input!="":
                setattr(self, attribute, user_input)

    def set_employee_id(self, id):
        self.id = id

    def set_employee_title(self, title):
        self.title = title

    def set_forename(self, forename):
        self.forename = forename

    def set_surname(self, surname):
        self.surname = surname

    def set_email(self, email):
        self.email = email

    def set_salary(self, salary):
        self.salary = salary

    def get_employee_id(self):
        return self.id

    def get_employee_title(self):
        return self.title

    def get_forename(self):
        return self.forename

    def get_surname(self):
        return self.surname

    def get_email(self):
        return self.email

    def get_salary(self):
        return self.salary

    def to_tuple(self, include_id=False):
        if include_id:
            return (
                    self.get_employee_title(),
                    self.get_forename(),
                    self.get_surname(),
                    self.get_email(),
                    self.get_salary(),
                    self.get_employee_id())
        else:
            return (self.get_employee_title(),
                    self.get_forename(),
                    self.get_surname(),
                    self.get_email(),
                    self.get_salary())

    def __str__(self):
        return make_employee_table(self)


def make_employee_table(employees: Iterable):

    table = PrettyTable()
    data_attributes = ['id'] + Employee.user_editable_attributes
    table.field_names = [a.capitalize() for a in data_attributes]

    if type(employees) is not list:
        employees = [employees]

    for e in employees:
        table.add_row([getattr(e, a) for a in data_attributes])

    return table
