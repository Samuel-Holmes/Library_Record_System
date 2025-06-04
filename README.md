# Library Management System

This is a simple command-line-based Library Management System written in Python. It allows librarians to manage book collections and user accounts, handling operations such as borrowing, returning, and updating records. The system stores all persistent data in a `data.json` file.


## Features

- 📚 **Book Management**
  - Add new books with metadata and available copy counts.
  - Search for books by title.
  - List all books in the collection.
  - Automatically prevents duplicate entries based on detailed metadata.
  - Tracks borrowing history and due dates.

- 👥 **User Management**
  - Add new users with validated personal details.
  - Update existing user details.
  - List all registered users.

- **Borrowing and Returning**
  - Borrow books by available copies.
  - Extend due date if a user tries to re-borrow the same book.
  - Return borrowed books and update availability.
  - Track which user borrowed which book and their due dates.


## Data Storage

All data is stored persistently in a JSON file:

```json
{
  "Books": [],
  "Users": []
}
```
This structure allows the application to track books and users between sessions. The file is automatically updated as operations are performed within the system.

## How to start the system

1. Ensure you have Python 3 installed on your system
2. This programme uses standard libraries so no further packages are required 
3. Clone this repository or download the files 
4. Open your command line or terminal and navigate to the file where the project is located
5. Run the command ```python library_system.py```



## Working the system

You will be prompted with a menu that includes:

Add a book

Borrow a book

Return a book

Find a book by title

List all books

Add a user

Update user details

List all users

Type the corresponding number to perform an action, or type 'q' to exit.




