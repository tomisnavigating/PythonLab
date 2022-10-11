import sqlite3


from employee import Employee
from userconfirmation import UserConfirmationProvider


class DBOperations:
    employee_table_name = "EmployeeUoB"

    sql_create_table = "CREATE TABLE EmployeeUoB (Id INTEGER PRIMARY KEY AUTOINCREMENT, Title, Forename, Surname, EmailAddress, Salary)"
    sql_check_table_exists = "SELECT * FROM sqlite_master WHERE name=?"
    sql_insert = "INSERT INTO EmployeeUoB (Title, Forename, Surname, EmailAddress, Salary) VALUES (?,?,?,?,?)"
    sql_select_all = "SELECT * from EmployeeUoB"
    sql_search_id = "SELECT * from EmployeeUoB where Id = ?"
    sql_search_name = "SELECT * from EmployeeUoB where Forename LIKE ? OR Surname LIKE ?"
    sql_update_data = "UPDATE EmployeeUoB SET Title=?,Forename=?, Surname=?, EmailAddress=?, Salary=? WHERE Id = ?"
    sql_delete_data = "DELETE FROM EmployeeUoB WHERE Id = ?"
    sql_salary_adjustment = "UPDATE EmployeeUoB SET Salary=Salary*? WHERE Id=?"
    sql_salary_adjustment_all = "UPDATE EmployeeUoB SET Salary=Salary*?"
    sql_drop_table = ""
    sql_get_last_id = "SELECT last_insert_rowid()"
    
    def __init__(self, database_name: str):
        try:
            self.database_name = database_name
            self.conn = sqlite3.connect(database_name)

        except Exception as e:
            print(e)

        finally:
            self.conn.close()

    def get_connection(self):
        self.conn = sqlite3.connect(self.database_name)
        self.cur = self.conn.cursor()

    def create_table_if_not_exists(self):
        try:
            if self.table_exists():
                print(f"Table <<{self.employee_table_name}>> not created: Table already exists")
            else:
                self.create_table()
                if self.table_exists():
                    print(f"Table <<{self.employee_table_name}>> created successfully")
                else:
                    print(f"Unable to create table <<{self.employee_table_name}>>")
        except Exception as e:
            print(e)

    def table_exists(self):
        try:
            self.get_connection()
            result = self.cur.execute(self.sql_check_table_exists, (self.employee_table_name,))
            tables_returned = result.fetchone()
            return tables_returned is not None
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def create_table(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_create_table)
            self.conn.commit()

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def insert_data(self, data_to_insert: Employee, confirmationProvider: UserConfirmationProvider):
        success = False
        try:
            self.get_connection()
            self.cur.execute(self.sql_insert, data_to_insert.to_tuple())

            self.cur.execute(self.sql_search_id, (self.cur.lastrowid,))
            inserted_data = Employee.from_db_result(self.cur.fetchone())

            if confirmationProvider.requestConfirmation(inserted_data):
                self.conn.commit()
                success = True 
            else:
                self.conn.rollback()

        except Exception as e:
            print(e)

        finally:
            self.conn.close()
            return success

    def select_all(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all)

            results = [Employee.from_db_result(r) for r in self.cur.fetchall()]

            return results

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def search_data_name(self, term):
        try:
            self.get_connection()

            term = "%" + term + "%"

            self.cur.execute(self.sql_search_name, (term, term))
            result = [Employee.from_db_result(r) for r in self.cur.fetchall()]
            return result

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def search_data_id(self, search_term: str):
        try:
            self.get_connection()

            self.cur.execute(self.sql_search_id, (search_term,))
            result = Employee.from_db_result(self.cur.fetchone()) 
            return result

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def update_data(self, employee: Employee, confirmationProvider: UserConfirmationProvider):
        success = False
        try:
            self.get_connection()

            self.cur.execute(self.sql_update_data, employee.to_tuple(include_id=True))

            self.cur.execute(self.sql_search_id, (employee.id,))
            updated_employee = Employee.from_db_result(self.cur.fetchone())

            if confirmationProvider.requestConfirmation(updated_employee):
                self.conn.commit()
                success = True

        except Exception as e:
            print(e)
            
        finally:
            self.conn.close()
            return success

    # Define Delete_data method to delete data from the table. The user will need to input the employee id to delete the corrosponding record.
    def delete_data(self, id: int, confirmationProvider: UserConfirmationProvider):
        success = False
        try:
            self.get_connection()

            self.cur.execute(self.sql_search_id, (id,))
            deleted_employee = Employee.from_db_result(self.cur.fetchone())     
            self.cur.execute(self.sql_delete_data, (id,))

            if confirmationProvider.requestConfirmation(deleted_employee):
                self.conn.commit()
                success = True
            else:
                self.con.rollback()

        except Exception as e:
            print(e)
        finally:
            self.conn.close()
            return success

    def adjust_pay(self, id: int, percentage_increase: float, confirmationProvider: UserConfirmationProvider):
        success = False
        try:
            self.get_connection()
            self.cur.execute(self.sql_salary_adjustment, (1 + percentage_increase / 100, id))

            self.cur.execute(self.sql_search_id, (id,))
            updated_employee = Employee.from_db_result(self.cur.fetchone())            

            if confirmationProvider.requestConfirmation(updated_employee):
                self.conn.commit()
                success = True
            else:
                self.conn.rollback()

        except Exception as e:
            print(e)
        finally:
            self.conn.close()
            return success

    def adjust_pay_all_employees(self, percentage_increase: float, confirmationProvider: UserConfirmationProvider):
        success = False
        try:
            self.get_connection()
            self.cur.execute(self.sql_salary_adjustment_all, (1 + percentage_increase / 100,))

            self.cur.execute(self.sql_select_all)
            updated_employees = [Employee.from_db_result(r) for r in self.cur.fetchall()]

            if confirmationProvider.requestConfirmation(updated_employees):
                self.conn.commit()
                success = True

        except Exception as e:
            print(e)
        finally:
            self.conn.close()
            return success



