# Import necessary libraries 
import uuid
import re
from datetime import datetime

# Regular expressions for validation
reg_name = r"^[a-zA-Z]+$"
reg_email = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$" 

# Books class
class Books:
    def __init__(self, title, author, year, publisher, availableCopies, publicationDate):
        self.bookID = uuid.uuid4()
        self.title = title 
        self.author = author 
        self.year = year 
        self.publisher = publisher 
        self.availableCopies = availableCopies 
        self.publicationDate = publicationDate 

# BookList class
class BookList:
    def __init__(self):
        self.book_list = {}
    
    def add_book_to_collection(self, book):
        if isinstance(book, Books):
            self.book_list[book.title] = book
        else:
            raise ValueError("Invalid book object")

# Users class
class Users:
    def __init__(self, username, firstname, surname, housenumber, streetname, postcode, emailaddress, dateofbirth):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.housenumber = housenumber
        self.streetname = streetname
        self.postcode = postcode
        self.emailaddress = emailaddress
        self.dateofbirth = dateofbirth

    def update_details(self):
        self.firstname = input("Enter new first name: ").strip() or self.firstname
        self.surname = input("Enter new surname: ").strip() or self.surname
        self.housenumber = input("Enter new house number: ").strip() or self.housenumber
        self.streetname = input("Enter new street name: ").strip() or self.streetname
        self.postcode = input("Enter new postcode: ").strip() or self.postcode
        email = input("Enter new email address: ").strip()
        if re.match(reg_email, email):
            self.emailaddress = email
        date_of_birth = input("Enter new date of birth (DD/MM/YYYY): ").strip()
        try:
            self.dateofbirth = datetime.strptime(date_of_birth, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format")

# UserList class
class UserList:
    def __init__(self):
        self.user_list = {}
    
    def add_user(self):
        username = input("Enter username: ").strip()
        if username.lower() == 'q':
            return
        firstname = input("Enter first name: ").strip()
        surname = input("Enter surname: ").strip()
        housenumber = input("Enter house number: ").strip()
        streetname = input("Enter street name: ").strip()
        postcode = input("Enter postcode: ").strip()
        emailaddress = input("Enter email address: ").strip()
        dateofbirth = input("Enter date of birth (DD/MM/YYYY): ").strip()
        try:
            dateofbirth = datetime.strptime(dateofbirth, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format, user not added")
            return
        user = Users(username, firstname, surname, housenumber, streetname, postcode, emailaddress, dateofbirth)
        self.user_list[username] = user
        print("User added successfully")

    def update_user(self, username):
        if username.lower() == 'q':
            return
        user = self.user_list.get(username)
        if user:
            user.update_details()
            print("User details updated successfully")
        else:
            print("User not found")

# Main Library Loop
def lib_loop():
    book_list = BookList()
    user_list = UserList()
    
    while True:
        print("\n Welcome to the library system:")
        print("1. Add a book")
        print("2. Add a user")
        print("3. Update user details")
        print("4. Exit system")
        print("(Press 'q' at any point to exit a prompt)")
        
        choice = input("Please select an option 1-4: ").strip()

        if choice.lower() == 'q':
            print("Exiting library system")
            break

        if choice == '1':
            title = input("Enter the book's title: ").strip()
            if title.lower() == 'q':
                continue
            author = input("Enter the author's name: ").strip()
            if author.lower() == 'q':
                continue
            year = input("Enter the book's year: ").strip()
            if year.lower() == 'q':
                continue
            publisher = input("Enter the book's publisher: ").strip()
            if publisher.lower() == 'q':
                continue
            availableCopies = input("Enter the number of available copies: ").strip()
            if availableCopies.lower() == 'q':
                continue
            publicationDate = input("Enter the publication date: ").strip()
            if publicationDate.lower() == 'q':
                continue
            book = Books(title, author, year, publisher, availableCopies, publicationDate)
            book_list.add_book_to_collection(book)
            print("Book added successfully")

        elif choice == '2':
            user_list.add_user()
        
        elif choice == '3':
            username = input("Enter the username to update: ").strip()
            if username.lower() == 'q':
                continue
            user_list.update_user(username)
        
        elif choice == '4':
            print("Exiting library system")
            break
        else:
            print("Invalid choice, please enter a number between 1-4")

# Run the loop
lib_loop()