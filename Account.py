
class Account:
    def __init__(self, uid, no_borrowed_books=0, no_reserved_books=0, no_returned_books=0, no_lost_books=0, fine_amount=0):
        """
        Initialize the Account object with user ID and account details.

        Parameters
        ----------
        uid : str
            The user ID.
        no_borrowed_books : int, optional
            The number of borrowed books (default is 0).
        no_reserved_books : int, optional
            The number of reserved books (default is 0).
        no_returned_books : int, optional
            The number of returned books (default is 0).
        no_lost_books : int, optional
            The number of lost books (default is 0).
        fine_amount : float, optional
            The fine amount on the account (default is 0).
        """
        self.uid = uid
        self.no_borrowed_books = no_borrowed_books
        self.no_reserved_books = no_reserved_books
        self.no_returned_books = no_returned_books
        self.no_lost_books = no_lost_books
        self.fine_amount = fine_amount

    def calculate_fine(self, days_overdue):
        """
        Calculate the fine based on the number of days overdue.

        Parameters
        ----------
        days_overdue : int
            The number of days overdue.

        Returns
        -------
        fine : float
            The calculated fine amount.
        """
        fine = days_overdue * 1
        self.fine_amount += fine
        return fine

    def pay_fine(self, db, amount):
        """
        Pay the fine by updating the fine amount in the database.

        Parameters
        ----------
        db : Database
            The database object to perform the fine payment.
        amount : float
            The amount to be paid for the fine.

        Returns
        -------
        None
        """
        account_obj = db.get_account(self.uid)
        current_fine = self.fine_amount

        if amount > current_fine:
            print(
                "The entered amount is greater than the fine amount.")
        elif amount <= 0:
            print("Please enter a positive amount to pay the fine.")
        else:
            new_fine_amount = current_fine - amount
            db.update_fine(self.uid, new_fine_amount)
            print(
                f"Fine payment of ${amount} successful. Remaining fine amount: ${new_fine_amount}")

