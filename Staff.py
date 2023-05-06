from User import User


class Staff(User):
    def __init__(self, uid, name, password, department):
        super().__init__(uid, name, password, "staff")
        self.department = department

    def foo(self):
        print("Foo")

    def menu(self, db):
        while True:
            print("""
                1. Option 1
                2. Option 2 ~List borrowed books
                3. Option 3 ~Add book
                4. Option 4 ~User record
                q. Return
                """)

            choice = input("Select your choice: ")
            f = {
                "1": self.foo,
                "2": self.foo,
                "3": self.foo,
                "q": "Quit",
            }.get(choice, None)

            if f == None:
                print("Error, try again...")
            elif f == "Quit":
                break
            else:
                f()
