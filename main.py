from databaseoperations import DBOperations
from employee import Employee, make_employee_table
from userconfirmation import UserConfirmationProvider


def get_numerical_user_input(data_type: type, prompt: str, minimum_value=None, maximum_value=None):
    """A helper function which retrives user input of a required type, with optional maximum
    and minimum values

    Args:
        data_type (type): The required data type (eg, int, float)
        prompt (str): The prompt to be shown to the user
        minimum_value : The minumum value a user is allowed to enter
        maximum_value : The maximum value a user is allowed to enter

    Returns:
        data_type: numerical data of hte requested type.
    """    
    while True:
        try:
            result = data_type(input(prompt + ":\t"))
            if minimum_value is not None:
                if result < minimum_value:
                    raise Exception(f"Enter a number greater than {minimum_value}")
                    continue
            if maximum_value is not None:
                if result > maximum_value:
                    raise Exception(f"Enter a number less than {maximum_value}")
                    continue
            return result

        except ValueError:
            print("Invalid numerical entry")
        except Exception as e:
            print(e)




def main():
    """
    The main function will parse arguments
    These arguments will be defined by the users on the console
    The user will select a choice from the menu to interact with the database.
    All input and output will be retrieved and produced by this function and supporting functions
    so that the class which accesses the database can remain as generic as possible.
    """    
    while True:
        print("\n Menu:")
        print("**********")
        print(" 1. Create table EmployeeUoB")
        print(" 2. Insert data into EmployeeUoB")
        print(" 3. Select all data from EmployeeUoB")
        print(" 4. Search for an employee")
        print(" 5. Update a record")
        print(" 6. Delete a record")
        print(" 7. Adjust an employee's pay")
        print(" 8. Adjust all employees' pay")
        print(" 9. Exit\n")

        try:
            __choose_menu = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input")
            continue

        db_ops = DBOperations("EmployeeDatabase.db")

        if __choose_menu == 1:  # create table
            db_ops.create_table_if_not_exists()

        elif __choose_menu == 2:  # insert new record

            data = Employee.from_user_input()
            confirmationProvider = UserConfirmationProvider("Confirm data insertion")

            if db_ops.insert_data(data, confirmationProvider):
                print("Data insertion successful")
            else:
                print("Data insertion failed")

        elif __choose_menu == 3:  # show all records
            print(make_employee_table(db_ops.select_all()))

        elif __choose_menu == 4:  # search database
            print("Enter number to search by Id or text to search within employee names.")
            search_term = input("Search For:\t")
            try:
                result = db_ops.search_data_id(int(search_term))
                if result is not None:
                    print(make_employee_table(result))

            except ValueError:
                result = db_ops.search_data_name(search_term)
                if len(result) != 0:
                    print(make_employee_table(result))

            

        elif __choose_menu == 5:  # update a record

            input_id = get_numerical_user_input(int, "Enter Employee ID", 0, None)

            employee_to_update = db_ops.search_data_id(input_id)

            if employee_to_update is not None:

                confirmationProvider = UserConfirmationProvider("Confirm update to record")
                employee_to_update.apply_user_update()

                if db_ops.update_data(employee_to_update, confirmationProvider):
                    print("Update successful")
                else:
                    print("Update unsucessful")

            else:
                print("No such record")  

        elif __choose_menu == 6: # delete a record

            input_id = get_numerical_user_input(int, "Enter Employee ID:\t", 0, None)

            employee_to_update = db_ops.search_data_id(input_id)

            if employee_to_update is not None:

                confirmationProvider = UserConfirmationProvider("Confirm deletion of record")

                if db_ops.delete_data(input_id, confirmationProvider):
                    print("Deletion successful")
                else:
                    print("Deletion unsucessful")

            else:
                print("No such record")


        elif __choose_menu == 7: # adjust an employee's pay

            input_id = get_numerical_user_input(int, "Enter Employee ID", 0, None)

            employee_to_award = db_ops.search_data_id(input_id)

            if employee_to_award is not None:

                input_percentage = get_numerical_user_input(float, "Enter percentage pay adjustment", -99.0, None)
                confirmationProvider = UserConfirmationProvider(
                    f"Confirm pay adjustment of {input_percentage}% for {employee_to_award.forename} {employee_to_award.surname}")

                db_ops.adjust_pay(input_id, input_percentage, confirmationProvider)

            else:
                print("No such record")


        elif __choose_menu == 8: # adjust all employees' pay

            input_percentage = float(input("Enter percentage pay adjustment:\t"))

            db_ops.adjust_pay_all_employees(input_percentage, UserConfirmationProvider("Confirm general pay adjustment"))


        elif __choose_menu == 9:
            exit(0)
        else:
            print("Invalid Choice")


if __name__ == "__main__":
    main()
