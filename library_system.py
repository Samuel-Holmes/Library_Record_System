"""
USERLIST AND BOOKLIST

remove data duplication by having these objects interact with books and users in the json storage respectively. there is no need to append them to two areas as opposed to one. Minimise it, have booklist interact with data['Books'] and userlist interact with data['users']

BOOKLIST 

borrow book method needs validation to check that the user exists before allowing them to borrow a book. needs to append to users borrowed books also. 
BOOK OBJECTS

validate that book does not already exist in the collection check against details such as title and publication date. This accounts for new editions of books also. 


** enhancing borrow and return book methods **
    
    when borrowing books check username against the user list in the json file (check is instance).

    allow to borrow and make sure to update borrowed by in book object, decrement the copies.

    set same for returning books, remove them from borrowed by, increment the copies. 

USER

add users to the json file only if they do not already exist.

add users to the userlist once they have passed this check. 

"""  






# importation of libraries used for the programme use cases commented next to each 

import uuid                                                  # creation of unique identifiers for each book object 
import re                                                    # used to match inputs to the regular expression format for validation purposes
import json                                                  # used as data storage for interaction with the json file 
from datetime import datetime, timedelta                     # used for date validation along with time changes for due dates 



# regular expression for email validation 

reg_email = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"


# opening and loading json file

with open("data.json", "r") as f:
    data = json.load(f)



# Utility functions

def get_input_string(prompt, validator=None, cast_type=str):
    while True:
        value = input(prompt).strip()
        if value.lower() == 'q':
            return None
        try:
            value = cast_type(value)
            if validator:
                if not validator(value):
                    print("Please try again.")
                    continue
            return value
        except ValueError:
            print("Please try again.")

def get_input_int(prompt, validator=None, cast_type=int):
    while True:
        
        value = input(prompt).strip()
        
        try:
            value = cast_type(value)
            if validator:
                if not validator(value):
                    print("Please try again.")
                    continue
            return value
        
        except ValueError:
            print("Please try again")
    

def is_valid_email(email):
    match = re.match(reg_email,email)

    if match:
        return True
    else:
        return False


def is_digit(value):
    
    if type(value) != int:
        print("Number entered must be a valid integer.")
        return False
    
    return True

def is_valid_pub_year(value):
    
    if len(str(value)) < 4:
        print("The year must be a valid 4 digit year.")
        return False
    
    return True

def parse_date(date_str):
    try:
        parsed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        return parsed_date.strftime("%d/%m/%Y")  
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return None
       


# Book class

class Book:
    def __init__(self, title, author, year, publisher, availableCopies, publicationDate):
        self.bookID = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.year = int(year)
        self.publisher = publisher
        self.availableCopies = int(availableCopies)
        self.publicationDate = publicationDate
        self.borrowed_by = []

    def to_dict(self):
        return {
            "bookID" : self.bookID,
            "title": self.title,
            "author" : self.author, 
            "year" : self.year,
            "publisher": self.publisher, 
            "availableCopies" : self.availableCopies, 
            "publicationDate" : str(self.publicationDate),
            "borrowed_by" : self.borrowed_by
        }
         


# BookList class      ******************************************************************FOCUS HERE NEXT************************************************************************************************************

class BookList:
    
    @classmethod    
    def find_book_by_title(cls,input):
        
        matched_books = []
        for book in data["Books"]:
            if book['title'].lower().strip() == input.lower().strip():
                matched_books.append(book)
        
        if matched_books:
            return matched_books 
        
        else:
            return "Book by that title has not been found"

    @classmethod
    def list_all_books(cls):
        
        for book in data['Books']:
            print(book)

    
    # check user exists also 
    @classmethod 
    def borrow_book(cls,book_id, username):
        
        for book in data['Books']:
            if book['bookID'] == book_id:
                if  book['availableCopies'] > 0:
                    due_date = datetime.now() + timedelta(days=14)
                    book['availableCopies'] -= 1
                    book['borrowed_by'].append({"username": username, "due_date": due_date})

                    print(f"Book borrowed successfully item is due on {due_date}")

                    with open("data.json", "w") as f:
                        json.dump(data,f,indent =2)
                    return
                
                else:
                    print("Book is not available currently please check back at a later time")
                    return

        print("Book with that ID was not found")
    
    def return_book(self, book_id, username):
        book = self.book_list.get(book_id)
        if book and username in book.borrowed_by:
            due_date = book.borrowed_by.pop(username)
            book.availableCopies += 1
            days_late = (datetime.now() - due_date).days
            if days_late > 0:
                print(f"Book returned {days_late} days late. Consider charging a fee.")
            else:
                print("Book returned on time. Thank you!")
        else:
            print("No record of this book being borrowed by you.")

    
    def remove_book_from_collection(self, title):
        pass


# User class

class User:
    def __init__(self, username, firstname, surname, housenumber, streetname, postcode, emailaddress, dateofbirth, borrowed_books):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.housenumber = housenumber
        self.streetname = streetname
        self.postcode = postcode
        self.emailaddress = emailaddress
        self.dateofbirth = dateofbirth
        self.borrowed_books = []

    def update_details(self):
        new_firstname = get_input_string("Enter new first name (or 'q' to exit): ")
        
        if new_firstname is None:
            print("Update cancelled.")
            return
        
        self.firstname = new_firstname

        new_surname = get_input_string("Enter new surname (or 'q' to exit): ")
        
        if new_surname is None:
            print("Update cancelled.")
            return
        
        self.surname = new_surname

        new_housenumber = get_input_int("Enter new house number (or 'q' to exit): ")
        
        if new_housenumber is None:
            print("Update cancelled.")
            return
        
        self.housenumber = new_housenumber

        new_streetname = get_input_string("Enter new street name (or 'q' to exit): ")
        
        if new_streetname is None:
            print("Update cancelled.")
            return
        
        self.streetname = new_streetname

        new_postcode = get_input_int("Enter new postcode (or 'q' to exit): ")
        
        if new_postcode is None:
            print("Update cancelled.")
            return
        
        self.postcode = new_postcode

        email = get_input_string("Enter new email address (or 'q' to exit): ", is_valid_email)
        
        if email is None:
            print("Update cancelled.")
            return
        
        self.emailaddress = email

        date_str = get_input_string("Enter new date of birth (DD/MM/YYYY) (or 'q' to exit): ")
        
        if date_str is None:
            print("Update cancelled.")
            return
        
        dob = parse_date(date_str)
        if dob:
            self.dateofbirth = dob
        else:
            print("Invalid date format. Date of birth not updated.")



# UserList class

class UserList:
    def __init__(self):
        self.user_list = {}

    def add_user(self):
        
        username = get_input_string("Enter username (or 'q' to exit): ")
        
        if not username:
            return
        
        firstname = get_input_string("Enter first name: ")
        surname = get_input_string("Enter surname: ")
        housenumber = get_input_int("Enter house number: ")
        streetname = get_input_string("Enter street name: ")
        postcode = get_input_int("Enter postcode: ")
        email = get_input_string("Enter email address: ", is_valid_email)
        dob_str = get_input_string("Enter date of birth (DD/MM/YYYY): ")
        dob = parse_date(dob_str)
        
        if not dob:
            print("Invalid date format. User not added.")
            return

        user = User(username, firstname, surname, housenumber, streetname, postcode, email, dob)
        self.user_list[username] = user
        print("User added successfully")

    def update_user(self, username):
        user = self.user_list.get(username)
        if user:
            user.update_details()
            print("User details updated successfully")
        else:
            print("User not found")

    def list_users(self):
        for user in self.user_list.values():
            print(f"{user.username}: {user.firstname} {user.surname}")


# Main loop
    

    while True:
        print("\nLibrary Menu:")
        print("1. Add a book")
        print("2. Add a user")
        print("3. Update user details")
        print("4. List all books")
        print("5. List all users")
        print("6. Borrow a book")
        print("7. Return a book")
        print("8. Exit")

        choice = input("Select an option 1-8: ").strip()

        if choice == '1':
            
            # creating the new book object getting user input 
            
            title = get_input_string("Enter book title: ")
            author = get_input_string("Enter author name: ")
            year = get_input_int("Enter year of publication: ", is_valid_pub_year)                  
            publisher = get_input_string("Enter publisher: ")
            copies = get_input_int("Enter number of copies: ", is_digit)
            
            while True:
                pub_date_str = get_input_string("Enter publication date (DD/MM/YYYY): ")
                
                if pub_date_str is None:
                    print("Book addition cancelled.")
                    break

                pub_date = parse_date(pub_date_str)

                if pub_date:
                    break
                else:
                    print("Please enter a valid date") 
            
            found = False  

            for book in data['Books']:
                if (book['title'].lower() == title.lower() and
                    book['author'].lower() == author.lower() and
                    book['year'] == year and
                    book['publisher'].lower() == publisher.lower() and
                    book['publicationDate'] == pub_date):
                    
                    print("Book item already exists in the collection. Please update details of the existing book.")
                    found = True
                    break

            # If no match was found, add the new book
            if not found:
                new_book = Book(title, author, year, publisher, copies, pub_date)
                book_dict = new_book.to_dict()

            # converting the book object to dictionary using created book method and appending to the data dictionary (json object to python dictionary)
            data["Books"].append(book_dict)
            
            # writing updated data to the json file 

            with open('data.json', 'w') as f:
                json.dump(data, f, indent=2)
            
            print("Book added successfully")


        elif choice == '2':
            user_list.add_user()

        elif choice == '3':
            username = get_input_string("Enter username to update: ")
            user_list.update_user(username)

        elif choice == '4':
            book_list.list_books()

        elif choice == '5':
            user_list.list_users()

        elif choice == '6':
            book_id = get_input_string("Enter book ID to borrow: ")
            username = get_input_string("Enter your username: ")
            book_list.borrow_book(book_id, username)

        elif choice == '7':
            book_id = get_input_string("Enter book ID to return: ")
            username = get_input_string("Enter your username: ")
            book_list.return_book(book_id, username)

        elif choice == '8':
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Please enter a number between 1-8.")

lib_loop()
