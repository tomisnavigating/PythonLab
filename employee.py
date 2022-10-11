from typing import Iterable

from prettytable import PrettyTable


class Employee:
    """
    The class which represents Employees. 
    """

    user_editable_attributes = ['title', 'forename', 'surname', 'email', 'salary']

    def __init__(self):
  
        self.id = 0
        self.title = ''
        self.forename = ''
        self.surname = ''
        self.email = ''
        self.salary = 0.0

    @staticmethod
    def from_user_input():
        """Static method which allows users to create Employee objects from the command line.

        Returns:
            Employee: A new Emplopyee object.
        """        
        e = Employee()

        for attribute in e.user_editable_attributes:
            setattr(e, attribute, input(f"{attribute.capitalize()}:\t"))

        return e

    @staticmethod
    def from_db_result(result_tuple):
        """Static method which allows an Employee object to be created from the result of an SQL query which returns a
        result from the EmployeeUoB table.

        Args:
            result_tuple (tuple): THe result of an SQL query over the EmployeeUoB table.

        Returns:
            Employee: A new Employee object
        """        
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
        """
        Function which allows the user to selectively update Employee attributes from the command line.
        """        
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
        """
        Function which returns the Employee object as a tuple of values which can be inserted into a SQL query wildcards.

        Args:
            include_id (bool, optional): Whether to include the Employee's Id in the tuple. Defaults to False.

        Returns:
            tuple: (title, forename, surname, email, salary, [id])
        """        
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

    """Creates a nicely formatted table of Employees from a list of Employee objects.

    Returns:
        str: String representation of a table of Employees, which can be printed to the console.

        Note: Uses the PrettyTable package: https://github.com/jazzband/prettytable
    """

    table = PrettyTable()
    data_attributes = ['id'] + Employee.user_editable_attributes
    table.field_names = [a.capitalize() for a in data_attributes]

    if type(employees) is not list:
        employees = [employees]

    for e in employees:
        table.add_row([getattr(e, a) for a in data_attributes])

    return table
