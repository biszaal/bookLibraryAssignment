from User import User


class Staff(User):
    def __init__(self, uid, name, password, department):
        super().__init__(uid, name, password, "staff")
        self.department = department

    def menu(self, db):
        super().menu(db)
