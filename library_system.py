"""
create a method to update available copies of a book by book ID

Look at the borrow book method in the BookList class methods, it needs to check if the book exists ideally append them to the matched books array if the length of the array is more than one librarian should be given the book details and choose which one matches the book to be borrowed. 


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
            return False
        
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

        if value.lower() == 'q':
            return False
        
        try:
            value = cast_type(value)
            if validator:
                if not validator(value):
                    print("Please try again.")
                    continue
            return value
        
        except ValueError:
            print("Please try again")

# This function is for saving updated data in temporary memory to the json file. 

def save():
    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)
    
    except IOError:
        print("Details could not be saved the system will now try resave the details.")
        re_save_details()

    else:
        print("Details saved successfully.")

# This function is for retrying a failed save attempt.

def re_save_details():
    try:
        with open("data.json", "w") as f:
            json.dump(data, f, indent=2)
        
    except IOError:
        print("Save was retried and failed again. Please manually record these details by hand. Attempt to update them again later using the old details.")

    else:
        print("Details saved successfully.")

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
        return False
       


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

# The method below is for adding a book to the collection.

    @classmethod
    def add_book_to_collection(cls):
        
        
        book_title_input = get_input_string("Book title: ")
        book_author_input = get_input_string("Author full name:  ")
        book_year_input = get_input_int("Book year: ", is_valid_pub_year)
        book_publisher_input = get_input_string("Publisher: ")
        book_available_copies_input = get_input_int("Available copies: ", is_digit)
        book_publication_date_input = get_input_string("Publication date in DD/MM/YYYY format: ", parse_date)

        try:
            book_details = Book(book_title_input,book_author_input,book_year_input,book_publisher_input,book_available_copies_input,book_publication_date_input)
            book_details_dictionary = book_details.to_dict()
            
        
        except ValueError:
            print("Some details are incorrect please try again.")
            book_details = None
            book_details_dictionary = None

        if book_details_dictionary:   
            
            for book in data['Books']:
            
                if (
                    book_details_dictionary['title'].lower().strip() == book['title'].lower().strip() 
                    and book_details_dictionary['author'].lower().strip() == book['author'].lower().strip() 
                    and book_details_dictionary['year'].lower().strip() == book['year'].lower().strip() 
                    and book_details_dictionary['publisher'].lower().strip() == book['publisher'].lower().strip() 
                    and book_details_dictionary['publicationDate'].strip() == book['publicationDate'].strip()
                    ):
                        print("Book with those details was already found in the collection. \nPlease use update book available copies menu choice and add extra copies.")
                        book_details = None
                        book_details_dictionary = None


            data['Books'].append(book_details_dictionary)
            save()
            print("Book added to collection successfully.")

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
    def borrow_book(cls):
        username = input("What is the name of the user that would like to borrow a book?: ")
        book_title = input("What is the title of the book the user would like to borrow?: ")
        matched_books = []
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
            
            if book['title'].lower().strip() == book_title.lower().strip():
                
                book_found = True
                matched_books.append(book)
                
                if book['availableCopies'] > 0:
                    due_date = datetime.now() + timedelta(days=14)
                    due_date = due_date.strftime("%d/%m/%Y")
                    book['availableCopies'] -= 1

                    book['borrowed_by'].append({"username": username, "due_date": due_date})
                    user_data['borrowed_books'].append({"bookID": book_id, "title": book['title'], "due_date": due_date})
                    
                    print(f"Book has been borrowed successfully and is due on: {due_date}")

                    save()

        if not book_found:
            print("Book with those details was not found. Please try again. If you are holding a physical copy of the book then available copies need updating before this transaction can proceed, there is an error in the inventory list.")


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
            return None

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

                save()
                
        if not book_found:
            print("Book with that ID was not found please try again.")
            


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
                return None
            
        
        firstname = get_input_string("Enter first name: ")
        surname = get_input_string("Enter surname: ")
        housenumber = get_input_int("Enter house number: ")
        streetname = get_input_string("Enter street name: ")
        postcode = get_input_string("Enter postcode: ")
        email = get_input_string("Enter email address: ", is_valid_email)
        dob_str = get_input_string("Enter date of birth (DD/MM/YYYY): ", parse_date)
        
        user = User(username, firstname, surname, housenumber, streetname, postcode, email, dob_str)
        user_dict = user.user_to_dict()

        data['Users'].append(user_dict)

        save()

    
# The method below allows for an upate of user details.     
    
    @classmethod
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
            return None
        
        user_data['username'] = get_input_string("Enter new username: ")
        user_data['firstname'] = get_input_string("Enter first name: ")
        user_data['surname'] = get_input_string("Enter surname: ")
        user_data['housenumber'] = get_input_int("Enter house number: ")
        user_data['streetname'] = get_input_string("Enter street name: ")
        user_data['postcode'] = get_input_string("Enter postcode: ")
        user_data['email'] = get_input_string("Enter email address: ", is_valid_email)
        user_data['dateofbirth'] = get_input_string("Enter date of birth (DD/MM/YYYY): ", parse_date)
        
            
        save()   

# The method below allows for the listing of all users
    
    @classmethod
    def list_users(cls):
        for user in data['Users']:
            print(f"Username: {user['username']}, User first and last name: {user['firstname']} {user['lastname']}")



        



# Main Loop 



def run_system():
    
    while True:
        
        print("\n1. Add a book to collection")
        print("2. Borrow a book")
        print("3. Return a book")
        print("4. Find a book by title")
        print("5. List all books")
        print("6. Add a user")
        print("7. Update user details")
        print("8. List all users")
        print(" ")
        
        choice = input("Please choose from the following options and enter a valid selection 1-8. Alternatively submit 'q' to exit the system: ").strip()

        if choice == 'q':
            break

        elif choice == '1':
            BookList.add_book_to_collection()

        elif choice == '2':
            BookList.borrow_book()

        elif choice == '6':
            UserList.add_user()






run_system()



