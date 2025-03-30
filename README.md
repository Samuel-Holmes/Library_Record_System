# Library_Record_System

## Video Demonstration Found in the Video's Folder of the Repository

### Overview

The Library System is a simple command-line application designed to manage books and users within a library. It allows librarians or users to add books to the collection, register new users, and update user details. The program provides an interactive menu to navigate different functionalities easily.

### Features

Add Books: Users can add books to the collection by providing relevant details such as title, author, year, publisher, available copies, and publication date.

Add Users: Users can be registered by entering their personal information such as name, address, email, and date of birth.

Update User Details: Registered users can update their personal information.

Exit Anytime: Users can exit the system or any prompt by entering 'q'.

### Technologies Used

Python 3: The entire application is written in Python.

UUID: Used to generate unique book IDs.

Regex (re): Used for validating email addresses.

Datetime: Used for handling date inputs.

### Installation & Setup

Ensure you have Python 3 installed on your system.

Download or clone the repository.

Navigate to the project directory and run the script:

python library_system.py

## How to Use:

Run the script.

Choose an option from the menu:

Press 1 to add a book.

Press 2 to add a new user.

Press 3 to update user details.

Press 4 to exit the system.

Follow the prompts to enter the required details.

At any point, you can enter 'q' to exit a prompt or the system.

### Example Usage

Welcome to the library system:
1. Add a book
2. Add a user
3. Update user details
4. Exit system
(Press 'q' at any point to exit a prompt)
Please select an option 1-4: 2
Enter username: john_doe
Enter first name: John
Enter surname: Doe
Enter house number: 123
Enter street name: Library St
Enter postcode: AB12 3CD
Enter email address: johndoe@example.com
Enter date of birth (DD/MM/YYYY): 15/06/1990
User added successfully!


### Future Enhancements

Implement book borrowing and returning functionality.

Add persistent storage using a database or file system.

Improve validation and error handling.

Implement a graphical user interface (GUI).
