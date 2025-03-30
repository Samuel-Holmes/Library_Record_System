'''
Student Name: Samuel Neil Holmes 
Student Code: BI64OI
'''


# Importation of the necessary libraries 

import uuid        # This lib will allow creation of our unique ID for each book object 
import re          # This lib will allow use of reg ex in firstname, surname, and email validation 
from datetime import datetime, timedelta # this lib allows the use of date calculations for due dates of loans along with validation of user DOB 

# Creation of regular expressions used in validation processes 
# email reg here is taken from the HTML 5 specification 

reg_name = "^[a-zA-Z]+$"
reg_email = "^[a-zA-Z0-9.!#$%&'*+=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"


# **** CREATION OF CLASSES *******


# books class, this will be the book objects and contain attributes related to particular book instances 

class Books: 

    # class constructor 

    def __init__(self, title, author, year, publisher, availableCopies, publicationDate):
        
        self.bookID = uuid.uuid4()
        self.title = title 
        self.author = author 
        self.year = year 
        self.publisher = publisher 
        self.availableCopies = availableCopies 
        self.publicationDate = publicationDate 

    # methods to get and set attributes defined below names are accurate description of what each method is responsible for here  

    def set_title(self):
        
        self.title = input("Please enter the book's title").strip()
        while not self.title: 
            self.title = input("This is not a valid title. Please enter a valid book title").strip()

    def get_title(self):
        return self.title

    
    def set_author(self):
        self.author = input("Please enter the author of this book?").strip()
        while not self.author:
            self.author = input("Please enter a valid author's name").strip()

    def get_author(self):
        return self.author

    def set_year(self):
        while True:
            try:
                self.year = int(input("Enter the year of this book"))
                break
            
            except ValueError:
                print("This is an invalid year please enter a valid year")

    def set_publisher(self):
        self.publisher = input("Please enter the publisher of this book").strip()
        while not self.publisher:
            self.publisher = input("This is an invalid publisher please enter the book publisher").strip()

    def get_publisher(self):
        return self.publisher


    def set_availableCopies(self):
        while True:
            try: 
                self.availableCopies = int(input("How many copies of this book does the library own that will be available to loan?"))
                break
            except ValueError:
                print("This is an invalid number of copies. Please enter an integer")

    def get_availableCopies(self):
        return self.availableCopies

    def set_publicationDate(self):
         while True:
            try:
                self.publicationDate = int(input("Enter publication date"))
                break
            except ValueError:
                print("This is an invalid publication year. Please enter a valid year")

    def get_publicationDate(self):
        return self.publicationDate

# booklist class, this class will be instance collations of current book instances. Essentially this becomes the entire library collection within the system. A dictionary data structure is initiated within the construction in which the book title becomes the key for the value pair this allows for easy manipulation 

class BookList: 

    def __init__(self):
        self.book_list = {}

    # methods below to add books to the list, search for books within the list, del books from the list, and check how many books are contained in the booklist using len()

    def add_book_to_collection(self,book):
        if isinstance(book,Books):
            self.book_list[book.title] = book
        else:
            raise ValueError("This book object does not exist within the library database")
    
    def search_book(self, search, search_term):

        found_books = []
        search = search.strip().lower()
        search_term = search_term.strip().lower()

        for book in self.book_list.values():
            if search_term == "title" and search == book.title.strip().lower():
                found_books.append(book)
            elif search_term == "author" and search == book.author.strip().lower():
                found_books.append(book)
            elif search_term == "publisher" and search == book.publisher.strip().lower():
                found_books.append(book)
            elif search_term == "publication date" and search == str(book.publicationDate):
                found_books.append(book)
            
        if found_books:
            print(found_books)
        else:
            return "No books matching those search criteria could be found"

    
    def del_book(self,title):
        if title in self.book_list:
            del self.book_list[title]
        else:
            raise ValueError(f"No book found with a title of {title}")

    def get_total_number_of_books(self):
        return len(self.book_list)


# users class, this class contains a constructor along with various methods for setting and getting attribute values 

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

# get attribute value methods


    def get_username(self):
        return self.username
    
    def get_firstname(self):
        return self.firstname

    def get_surname(self):
        return self.surname

    def get_housenumber(self):
        return self.housenumber

    def get_streetname(self):
        return self.streetname

    def get_postcode(self):
        return self.postcode

    def get_emailaddress(self):
        return self.emailaddress

    def get_dateofbirth(self):
        return self.dateofbirth


# methods for editing user attributes that include validation 

    def edit_firstname(self):
        new_firstname = input("Please enter what you would like this user's first name to be changed to").strip()

        if re.match(reg_name, new_firstname):
            self.firstname = new_firstname
        
        else:
            print("This is an invalid first name try again")

    def edit_surname(self):
        new_surname = input("Enter the surname that you would like this user's surname to be changed to").strip()

        if re.match(reg_name, new_surname):
            self.surname = new_surname

        else:
            print("This is an invalid surname")

    def edit_email(self):
        new_email = input("Please enter what you would like this users new email adress to be").strip()

        if re.match(reg_email, new_email):
            self.emailaddress = new_email

        else:
            print("This is not a valid email adress please try again")

    def edit_dateofbirth(self):
        new_dob = input("Enter new date of birth for this user in the format 'DD/MM/YYYY").strip()
        try: 
            validated_dob = datetime.strptime(new_dob, '%d/%m/%Y')
            self.dateofbirth = validated_dob
        
        except ValueError:
            print("This is not a valid date of birth format please try again!")

    
# userlist class this will be the collation of the individual user instances, constructor along with methods for adding users to list, removing users from the user list by first name and providing numbered options when there are more than one user with that name, count total users, and serach a users details by entering their username. Again here as with the booklist a dictionary data structure is used. This allows for easier manipulation

class UserList:

    def __init__(self):
        self.user_list = {}

    def add_user(self,user):
        if user.username in self.user_list:
            raise ValueError("User already exists within the libraries list of users")
        
        else:
            self.user_list[user.username] = user


# This method shown below is slightly more complex than the others so far, in essence it creates an empty list and loops through the user list dictionary values whilst checking whether the end user entered firstname matches a firstname within the dictionary

# If it does they are added to the empty list users_with_firstname. If there is more than one person in this list the user is given the option to delete based upon a displayed number. One is then subtracted from the presented number for indexing purposes.If there is not more than one user in the list then the else block at the bottom deals with this simple case just removing the singular user indexed at 0 
 
    def remove_user_by_firstname(self,firstname):

        users_with_firstname = []

        for user in self.user_list.values():
            if user.firstname == firstname:
                users_with_firstname.append(user)

        if not users_with_firstname:
            print(f"There were no user's with the name {firstname} found")
            return 
        
        if len(users_with_firstname) > 1:
            print("There has been more than one user found within the list with that firstname please select the number of the user you would like to remove")

            i = 1 
            for users in users_with_firstname:
                print(f"{i}. Username: {user.username}, Surname: {user.surname}, DOB: {user.dateofbirth}")
                i += 1

            try: 
                choose = int(input("Choose the number you would like to remove")) - 1

                if choose >= 0 and choose < len(users_with_firstname):
                    
                    removed = users_with_firstname[choose]
                    del self.user_list[removed.username]
                    print(f"The user {removed.username} was succesfully deleted")

                else: print("This choice is not valid")

            except ValueError:
                print("Invalid choice. Please input a valid number")

        else:
            removed = users_with_firstname[0]
            del self.user_list[removed.username]
            print(f"The user {removed.username} was succesfully deleted")


    
    def count_users_in_list(self):
        return len(self.user_list)
    
    def get_user_by_username(self,username):

        if username in self.user_list:
            return self.user_list[username]
        else:
            print("User was not found in the user list")
            return None
        


# loans class this will keep track of the loaned books allocated to each user. There are methods within this class for borrowing a book, returning a book, and for displaying overdue books. This in particular is where the datetime lib is used more extensively for date checking and time changes to calculate due dates. Again the empty loan record instance in the constructor is a dictionary for easy manipulation.  

class Loans:

    def __init__(self):
    
        self.borrowed_books = {}



    def borrow_book(self, user, book, days = 7):

        if user.username not in self.borrowed_books:
            self.borrowed_books[user.username] = []

            if book.availableCopies > 0:
                book_due = datetime.now() + timedelta(days = days)
                self.borrowed_books[user.username].append({'book': book.title, 'due_date': book_due})
                book.availableCopies -= 1
                print(f"The book {book.title} has been successfully borrowed")

            else:
                print("Sorry this book is not currently available")

    
    def return_book(self, user, book_title):

        if user.username not in self.borrowed_books:
            print("user currently has no borrowed books")
            return 
        
        found = False
        for record in self.borrowed_books[user.username]:
            if record['book'] == book_title:
                self.borrowed_books[user.username].remove(record)
                found = True
                print(f"This book has been succesfully returned ({book_title})")
                break
            
        if not found:
            print("This book was not found in this user's loan list")
        

def print_overdue_loans(self):

    for username, records in self.borrowed_books.items():
        for record in records:
            if datetime.now() > record['due_date']:
                print(f"{record['book']} should have been returned by this user on {record['due_date'].strftime('%d/%m/%Y')}")



# implementation of the main system loop

def lib_loop():
    
    book_list = BookList()
    user_list = UserList()
    loan = Loans()
    
    while True:
        print("\n Welcome to the library system:")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Edit a book")
        print("4. Search book")
        print("5. Add user")
        print("6. Remove user")
        print("7. Edit user")
        print("8. Borrow a book")
        print("9. Return a book")
        print("10. Display a users overdue books")
        print("11. Exit system")
        
        
        choice = input("Please select an option 1-11").strip()

        if choice == '1':
            title = input("enter the book's title: ").strip().lower()
            author = input("enter the author's name: ").strip().lower()
            year = input("enter the book's year: ")
            publisher = input("enter the book's publisher: ").strip().lower()
            availableCopies = input("enter the book's number of available copies: ")
            publicationDate = input("enter the book's publicationDate: ")
            book = Books(title, author, year, publisher, availableCopies, publicationDate)
            book_list.add_book_to_collection(book)
            print("this book has been added to the collection")

        elif choice == '2':
            title = input("please enter the title of the book you would like to remove: ")

            try:
                book_list.del_book(title)
                print("book has been removed")

            except ValueError: 
                print("no book has been found with this title")

        elif choice == '3':
            title = input("please enter the title of the book you would like to edit: ")
            book = book_list.book_list.get(title)

            if book: 
                print("\n please select what you would like to edit from the following options: ")

                print("1. title")
                print("2. author")
                print("3. year")
                print("4. publisher")
                print("5. available copies")
                print("6. publication date")

                edit_choice = input("please choose a number between one and 6: ").strip()

                if edit_choice == '1':
                    book.set_title()
                
                elif edit_choice == "2":
                    book.set_author()

                elif edit_choice == "3":
                    book.set_year()

                elif edit_choice == "4":
                    book.set_publisher()

                elif edit_choice == "5":
                    book.set_availableCopies()

                elif edit_choice == "6":
                    book.set_publicationDate()

                else:
                    print("not a valid option")



        elif choice == '4':
            
            search_term = input("would you like to search by title, author, publisher, or publication date?: ")
            search = input("okay please enter the search term: ")

            result = book_list.search_book(search, search_term)
            print(result)


        elif choice == '5':
            
            username = input("enter username: ").strip()
            firstname = input("enter first name: ").strip()
            surname = input("enter the surname: ").strip()
            housenumber = input("enter house number: ")
            streetname = input("enter street name: ").strip()
            postcode = input("enter postcode: ").strip()
            emailadress = input("enter email address: ")
            dateofbirth = input("enter date of birth (DD/MM/YYYY)")
            user = Users(username, firstname, surname, housenumber, streetname, postcode, emailadress, dateofbirth)
            user_list.add_user(user)
            print("this user has been added to the user list")

        
        elif choice == '6':
            firstname = input("enter the first name of the user to remove: ").strip()
            user_list.remove_user_by_firstname(firstname)

        elif choice == '7':
            username = input("enter the username of the user to edit: ").strip()
            user = user_list.get_user_by_username(username)

            if user:
                print("\n what would you like to edit")
                print("1. first name")
                print("2. surname")
                print("3. email")
                print("4. date of birth")

                editing_choice = input("please select an option 1-4: ").strip()

                if editing_choice == '1':
                    user.edit_firstname()

                elif editing_choice == "2":
                    user.edit_surname()

                elif editing_choice == "3":
                    user.edit_email()

                elif editing_choice == "4":
                    user.edit_dateofbirth()
                
                else:
                    print("invalid choice")

        elif choice == '8':
            username = input("please input your username to borrow a book: ").strip()
            user = user_list.get_user_by_username(username)

            if user:
                title = input("enter the title of the book you want to borrow please: ").strip().lower()
                book = book_list.book_list.get(title)

                if book:
                    loan.borrow_book(user, book)

                else:
                    print("this book is not in the library")

            else: 
                print("user not found in system")

        elif choice == '9':
            username = input("please enter your username in order to return a borrowed book: ").strip()
            user = user_list.get_user_by_username(username)

            if user:
                book_title = input("enter the title of the book you wish to return: ")
                loan.return_book(user, book_title)

            else:
                print("user not found")


        elif choice == '10':
            username = input("enter yor username to display your overdue books")
            user = user_list.get_user_by_username(username)

            if user:
                loan.print_overdue_loans(user)

            else:
                print("user not found")

        elif choice == '11':
            print("you are exiting the library system")
            break
    
        else:
            print("invalid choice please enter a number between one and eleven")


# run the loop 

lib_loop()