from User import User


class Staff(User):
    def __init__(self, uid, name, password, department):
        """
        Initialize the Staff object with user ID, name, password, and department.

        Parameters
        ----------
        uid : int
            The unique user ID.
        name : str
            The staff member's name.
        password : str
            The staff member's password.
        department : str
            The staff member's department.
        """
        super().__init__(uid, name, password, "staff")
        self.department = department

    def menu(self, db):
        """
        Display the staff menu and handle user input for performing various actions.
        Inherits the menu method from the User class as both Staff and Student have the same options.

        Parameters
        ----------
        db : object
            The database object.

        Returns
        -------
        None
        """
        super().menu(db)
