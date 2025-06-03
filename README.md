### System Design and Requirements

I undertook this project in order to solidify my understanding of and gain practise in OOP within the Python programming language. I focused on attempting to replicate a useable system that mimicked a real world system so I could understand the necessary interactions and functionalities needed within a traditional system. The sys contains classes such as Books, BookList, Users and UserList they have the following uses:

* Books: This class allows for the instantiation of book objects within the programme. During construction they are assigned user inputted attributes such as title, author, publication date etc. In addition there is a method for converting the object to a dictionary for storage in the json file.

* BookList: This class can be viewed as the library collection itself. Rather than being instances of objects it simply contains methods that can be used to interact with the book objects such as adding a book to the collection, borrowing a book, returning a book etc. 

* Users: This class is for instantiating user objects. With attributes such as username, user email, first name, last name etc.
