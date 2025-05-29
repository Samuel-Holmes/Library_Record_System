"""
USERLIST AND BOOKLIST

remove data duplication by having these objects interact with books and users in the json storage respectively. there is no need to append them to two areas as opposed to one. Minimise it, have booklist interact with data['Books'] and userlist interact with data['users']

add a way to remove books from the collection in the booklist class 

USER

add users to the json file only if they do not already exist.

add users to the userlist once they have passed this check. 

"""  






# Importation of libraries: 

# creation of unique identifiers for each book object
import uuid                                                   

# used to match inputs to the regular expression format for validation purposes
import re

# used as data storage for interaction with the json file 
import json

# used for date validation along with time changes for due dates 
from datetime import datetime, timedelta                    



# Regular expression for email validation: 

reg_email = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"


# Opening and loading json file:

with open("data.json", "r") as f:
    data = json.load(f)



# Utility functions:

# This function allows for getting string inputs, it includes a validator as a parameter so a validator can be passed as an argument.

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



# This function allows for getting integer inputs, similar to above includes a validator when passed as an argument.

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
    


# This function is for validating emails received during get_input_string function call.

def is_valid_email(email):                                                                 
    match = re.match(reg_email,email)

    if match:
        return True
    else:
        return False



# This function verifies valid integers when passed to the get_input_int function.

def is_digit(value):                                                                        
    
    if type(value) != int:
        print("Number entered must be a valid integer.")
        return False
    
    return True


# This function ensures that publication year length is not less than 4 digits in length.

def is_valid_pub_year(value):                                                                
    
    if len(str(value)) < 4:
        print("The year must be a valid 4 digit year.")
        return False
    
    return True


# This function checks validity of dates DD/MM/YYYY it attempts to create a date object from the users input. If it succeeds date is returned as a string. If it fails the error message is presented.

def parse_date(date_str):                                                                  
    
    try:
        parsed_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        return parsed_date.strftime("%d/%m/%Y")  
    
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return None
       


# Book class:

class Book:

# The constructor that implements unique IDs to the book objects along with other attributes 
    
    def __init__(self, title, author, year, publisher, availableCopies, publicationDate):
        self.bookID = str(uuid.uuid4())
        self.title = title
        self.author = author
        self.year = int(year)
        self.publisher = publisher
        self.availableCopies = int(availableCopies)
        self.publicationDate = publicationDate
        self.borrowed_by = []

# The method below converts the Book instances to a dictionary format to allow for easy access and storage within the data.json file.

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
         


# BookList class:

class BookList:

# The method below is for finding a book within data['Books'] by title entered by the end user. It checks if the book exists and if it does it appends that to a list matched books which is returned by the method. Otherwise, it will alert the user that a book with that title does not exist.

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


# This method iterates over and prints all books with the data['Books] list
   
    @classmethod
    def list_all_books(cls):
        
        for book in data['Books']:
            print(book)

# This method allows for the borrowing of books, it checks both the user exists and the book exists in the collection before it can be borrowed. It then decrements the available copies appropriately, updates the books borrowed by and users borrowed books attributes appropriately.

    @classmethod 
    def borrow_book(cls,book_id, username):
        
        user_exists = False
        user_data = None

        for user in data['Users']:
            
            if user['username'] == username:
                user_exists = True
                user_data = user
                break
        
        if not user_exists:
            
            print("User with those details does not exist. Please try again")
            return
        
        
        book_found = False
        for book in data['Books']:
            
            if book['bookID'] == book_id:
                
                book_found = True
                
                if book['availableCopies'] > 0:
                    due_date = datetime.now() + timedelta(days=14)
                    due_date = due_date.strftime("%d/%m/%Y")
                    book['availableCopies'] -= 1

                    book['borrowed_by'].append({"username": username, "due_date": due_date})
                    user_data['borrowed_books'].append({"bookID": book_id, "title": book['title'], "due_date": due_date})
                    
                    print(f"Book has been borrowed successfully and is due on: {due_date}")

                    try: 
                        with open("data.json", "w") as f:
                            json.dump(data, f, indent=2)
                    
                    except IOError:
                        print("Error saving data to file")

                    return

        if not book_found:
            print("Book with those details was not found. Please try again. If you are holding a Physical copy of the book then available copies need updating before this transaction can proceed, there is an error in the inventory list.")


# This method allows for book returns, again it checks that both the user and book objects exist. It then appropriately updates the neccessary attributes and increments available copies.   
    
    @classmethod
    def return_book(cls, book_id, username):
        
        user_exists = False
        for user in data['Users']:
            if user['username'] == username:
                user_exists = True
                user_data = user
                break
        
        if not user_exists:
            print("User with those details does not exist. Please try again.")
            return False

        book_found = False
        
        for book in data['Books']:
            if book['bookID'] == book_id:
                book_found = True
                new_borrowed_by = []
                

                for item in book['borrowed_by']:
                    if item['username'] != username:
                        new_borrowed_by.append(item)

                book['borrowed_by'] = new_borrowed_by
                book['availableCopies'] += 1

                
                new_borrowing_user_record = []
                for record in user_data['borrowed_by']:
                    if record['bookID'] != book_id:
                        new_borrowing_user_record.append(record)

                
                user_data['borrowed_books'] = new_borrowing_user_record

                
                try: 
                    with open("data.json", "w") as f:
                        json.dump(data, f, indent=2)
                    
                except IOError:
                    print("Error saving data to file")

                
                print("Book returned successfully.")
                return True 


        if not book_found:
            print("Book with that ID was not found please try again.")
            return False


# User class

class User:

# The constructor allowing for User object instances to be created. 
    
    def __init__(self, username, firstname, surname, housenumber, streetname, postcode, emailaddress, dateofbirth):
        self.username = username
        self.firstname = firstname
        self.surname = surname
        self.housenumber = housenumber
        self.streetname = streetname
        self.postcode = postcode
        self.emailaddress = emailaddress
        self.dateofbirth = dateofbirth
        self.borrowed_books = []

# The method below is used to convert the User objects to dictionaries for access and storage within the data.json file.      
    
    def user_to_dict(self):
        return {
            "username" : self.username,
            "firstname": self.firstname,
            "surname" : self.surname, 
            "housenumber" : self.housenumber,
            "streetname": self.streetname, 
            "postcode" : self.postcode, 
            "emailadress" : self.emailaddress,
            "dateofbirth" : self.dateofbirth,
            "borrowed_books" : self.borrowed_books
        }
   

# UserList class

class UserList:

# The method below allows for creation of user objects based upon user input. i.e they input the arguments passed to the constructor above. This contains validation to prevent duplicates and invalid dates of birth it then writes the updated data to the json file.      
    
    @classmethod
    def add_user(cls):
        
        username = get_input_string("Enter username (or 'q' to exit): ")
        
        if not username or username.lower() == 'q':
            return
        
        for user in data['Users']:
            if username == user['username']:
                print("A user with that username already exists")
                return False
            
        
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
            return False


        user = User(username, firstname, surname, housenumber, streetname, postcode, email, dob)
        user_dict = user.user_to_dict()

        data['Users'].append(user_dict)

        try:
            with open("data.json", "w") as f:
                json.dump(data, f, indent=2)
        
        except IOError:
            print("User data could not be written to storage")

        print("User added successfully")
        return True

    
# The method below allows for an upate of user details.     
    
    def update_user_details(cls, username):
        user_data = None   
        user_found = False
        
        for user in data['Users']:
            if username == user['username']:
                user_found = True
                user_data = user 
                break
            
        if not user_found:
            print("User with that username was not found in the system")
        else:
            return user_data
        
        user_data['username'] = get_input_string("Enter new username: ")
        user_data['firstname'] = get_input_string("Enter first name: ")
        user_data['surname'] = get_input_string("Enter surname: ")
        user_data['housenumber'] = get_input_int("Enter house number: ")
        user_data['streetname'] = get_input_string("Enter street name: ")
        user_data['postcode'] = get_input_int("Enter postcode: ")
        user_data['email'] = get_input_string("Enter email address: ", is_valid_email)
        dob_str = get_input_string("Enter date of birth (DD/MM/YYYY): ")
        dob = parse_date(dob_str)

        if dob:
            user_data['dateofbirth'] = dob
            
           

    def list_users(self):
        pass



# Main Loop 

def run_system():
    pass
