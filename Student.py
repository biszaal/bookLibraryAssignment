from User import User


class Student(User):
    def __init__(self, uid, name, password, studentClass):
        super().__init__(uid, name, password, "student")
        self.studentClass = studentClass

    # I have implemented menu to the User because both Staff and Student has the same options
    def menu(self, db):
        super().menu(db)
