from employee import make_employee_table

class UserConfirmationProvider:
    """The UserConfirmationProvider class provides a way to pass in a callback to 
    DBOperations functions which can be used to solicit confirmation from the user
    that the changes that are being made are correct.
    The use of UserConfirmationProviders mean that there is no user interaction code 
    (eg: input or print statements) within the DBOperations class, and so ultimately this class could be re-used in a 
    non-CLI application.
    """    

    def __init__(self, prompt: str) -> None:
        self.prompt = prompt

    def requestConfirmation(self, data):
        """Ask for confirmation of the changes.

        Args:
            data ([]Employee]): A list of the affected Employee records

        Returns:
            bool: Whether the user approved the change(s)
        """        
        print("\nAffected data")
        print(make_employee_table(data))

        operation_confirmed = None
        while operation_confirmed is None:
            response = input(f"{self.prompt} [y/n]: ")
            if response in ["y", "Y"]: operation_confirmed = True
            if response in ["n", "N"]: operation_confirmed = False

        return operation_confirmed

        