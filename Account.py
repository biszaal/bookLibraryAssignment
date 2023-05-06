
class Account:
    def __init__(self, uid, no_borrowed_books=0, no_reserved_books=0, no_returned_books=0, no_lost_books=0, fine_amount=0):
        self.uid = uid
        self.no_borrowed_books = no_borrowed_books
        self.no_reserved_books = no_reserved_books
        self.no_returned_books = no_returned_books
        self.no_lost_books = no_lost_books
        self.fine_amount = fine_amount

    def calculate_fine(self, days_overdue):
        fine = days_overdue * 1
        self.fine_amount += fine
        return fine

    def pay_fines(self, amount):
        if amount <= self.fine_amount:
            self.fine_amount -= amount
            print(
                f"You have paid ${amount}. Remaining fines: ${self.fine_amount}")
        else:
            print("Invalid payment amount")

    def menu(self, db):
        pass
