from User import User


class Student(User):
    def __init__(self, uid, name, password, studentClass):
        super().__init__(uid, name, password, "student")
        self.studentClass = studentClass

    def menu(self, db):
        print("""
            1. Option-1
            2. Option-2
            3. Option-3
            q. Quit
            """)
