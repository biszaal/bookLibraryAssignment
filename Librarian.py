from User import User


class Librarian(User):
    def __init__(self, uid, name):
        super().__init__(uid, name)

    def search(self, db):
        opt = input("Enter search type (title/authors): ")
        s = input("Enter search query: ")
        results = db.search(opt, s)
        for r in results:
            print(r)

    def menu(self, db):
        while True:
            print("""
                1. Search catalogue
                2. Check out books
                3. Reserve books
                4. Renew a book
                5. Return books
                6. View user records
                q. Quit
                """)
            choice = input("Select your choice: ")
            if choice == 'q':
                break
            elif choice == '1':
                self.search(db)
            elif choice in ['2', '3', '4', '5', '6']:
                print("Feature not implemented yet")
            else:
                print("Invalid choice")
