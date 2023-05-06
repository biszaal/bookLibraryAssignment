import json
import random
from datetime import datetime, timedelta
from Book import Book
from User import User
from Student import Student
from Staff import Staff
from Librarian import Librarian
from Account import Account
from LibDatabase import LibDatabase


class LibManSystem:
    def __init__(self):
        self.database = LibDatabase()
        self.database.create_books_table()
        self.database.create_users_table()
        self.database.create_accounts_table()
        self.load_books()
        self.load_users()
        self.menu()

    def menu(self):
        while True:
            print("Welcome to the Library Management System")
            print("1. Login")
            print("2. Register")
            print("3. Exit")
            choice = input("Enter your choice (1, 2, or 3): ")
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def register(self):
        print("Create a new account")
        uid = input("Enter a uid: ")
        name = input("Enter your name: ")
        password = input("Enter a password: ")
        uType = input(
            "Enter user type (student, staff, or librarian): ").lower()
        studentClass = None
        department = None

        user_obj = None

        if (uType == "student"):
            studentClass = input("Enter name of your class: ").lower()
            user_obj = Student(uid, name, password, studentClass)
        elif (uType == "staff"):
            department = input("Enter name of your department: ").lower()
            user_obj = Staff(uid, name, password, department)

        try:
            self.database.insert_user(user_obj)
            print("User created successfully. Please login.")
        except ValueError as e:
            print(f"Error in LibManSystem: {e}")
            print("Failed to create user. Please try again.")

    @staticmethod
    def authenticate(db, uid, password):
        user = User.load_user(db, uid)
        if user:
            print(f"User loaded: {user.uid}, {user.password}")
            if user.password == password:
                return user
        print("User not found or incorrect password.")
        return None

    def login(self):
        while True:
            print("Welcome...")
            uid = input("User ID: ")
            password = input("Password: ")
            user = self.authenticate(self.database, uid, password)
            if user:
                print(f"Welcome, {user.name}!")
                user.menu(self.database)
            else:
                print("Login failed. Please try again.")

    def load_books(self):
        with open('books.json') as f:
            books = json.load(f)
            for book in books:
                authors = book["authors"]
                available = random.randint(0, 10)
                book_obj = Book(book["isbn"], book["title"], book["publisher"], book["authors"],
                                available=available)
                self.database.insert_book(book_obj)

    def load_users(self):
        with open('login.json') as f:
            users = json.load(f)
            for uid, data in users.items():
                print(
                    f"Trying to load account: {uid}, {data['password']}, {data['name']}, {data['uType']}")

                user_obj = None
                if data["uType"] == "staff":
                    user_obj = Staff(
                        uid, data["name"], data["password"], data["department"])
                elif data["uType"] == "student":
                    user_obj = Student(
                        uid, data["name"], data["password"], data["studentClass"])
                existing_user = self.database.get_user(uid)
                if not existing_user:
                    self.database.insert_user(user_obj)
                    print(f"User {uid} loaded into the database.")
                else:
                    print(
                        f"User {uid} already exists in the database. Skipping.")

    def close(self):
        self.database.close()
        print("Database connection closed.")
