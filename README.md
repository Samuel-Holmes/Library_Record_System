
## Library System (Terminal-Based)

A simple, beginner-friendly Python terminal application for managing a basic library. It allows you to add books and users, borrow and return books, and update user information.

---

## Features

- Add and list books
- Add and list users
- Borrow and return books (with due date and late return warning)
- Update user details
- Input validation for dates, emails, and numbers
- Simple, interactive menu-driven interface

---

## How to Run

Make sure you have Python 3 installed, then run:

```bash
python library_system.py
```

Follow the terminal prompts to interact with the system.

---

## Main Menu Options

 1       Add a new book                      
 2       Add a new user                      
 3       Update an existing user's details   
 4       List all books                      
 5       List all users                      
 6       Borrow a book                       
 7       Return a borrowed book              
 8       Exit the system                     

---

## Classes Overview

### `Book`
Represents a book in the library.

- `bookID`: Unique ID (UUID)
- `title`, `author`, `year`, `publisher`, `availableCopies`, `publicationDate`
- `borrowed_by`: Dictionary tracking borrowed status (`username` → `due_date`)

### `BookList`
Manages the collection of books.

- `add_book_to_collection(book)`
- `list_books()`
- `find_book_by_title(title)`
- `borrow_book(book_id, username)`
- `return_book(book_id, username)`

### `User`
Represents a library user.

- Includes personal details and date of birth
- `update_details()` to interactively update the user

### `UserList`
Manages the collection of users.

- `add_user()`
- `update_user(username)`
- `list_users()`

---

## Input Validation

- Email is validated with a regex.
- Dates must follow `DD/MM/YYYY` format.
- Year and copy count must be numeric.

---

## Tips

- Enter `'q'` during any prompt to cancel that operation.
- Book IDs are shown when books are listed—keep them handy for borrow/return.
