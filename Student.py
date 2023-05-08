from User import User


class Student(User):
    def __init__(self, uid, name, password, studentClass):
        """
        Initialize the Student object with user ID, name, password, and student class.

        Parameters
        ----------
        uid : int
            The unique user ID.
        name : str
            The student's name.
        password : str
            The student's password.
        studentClass : str
            The student's class.
        """
        super().__init__(uid, name, password, "student")
        self.studentClass = studentClass

    def menu(self, db):
        """
        Display the student menu and handle user input for performing various actions.
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
