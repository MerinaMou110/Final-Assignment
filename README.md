                                                 Book Destiny - Library Management System
Welcome to Book Destiny, a comprehensive Library Management System designed to simplify the process of managing and accessing books within a library. This project is developed as part of an academic assignment, and it demonstrates my skills in Python, Django, and web development.

Features
1. User Management :
User Registration, Login & Logout: Secure and efficient user registration system with email verification.
Email Verification: Users receive a verification link via email. Accounts are activated upon clicking the link, allowing users to log in and access their profiles.
2. Book Management :
Book Catalog: A detailed catalog of books, including title, author, ISBN, publication date, genre, and availability status.
Book Search: A convenient search feature enabling users to find books by title.
3. Borrowing and Returning Books :
Borrowing System: Users can borrow books, and the system automatically updates the availability by reducing the book quantity.
Returning Books: Upon returning a book, users can leave a review, and the book quantity is incremented back.
4. Wishlist Management :heart: 
Reservation System: Users can add books to their wishlist for easy access and future reference.
5. Deployment and Submission :render: 
Deployed on a Secure and Scalable Platform: The project is deployed on a reliable hosting service, ensuring security and scalability.
Smooth User Experience: Ensures smooth browsing, book selection, and user interactions.
Project Documentation: Comprehensive documentation is provided for easy understanding and future enhancements.
Installation
To run the project locally, follow these steps:

Clone the repository:

git clone https://github.com/yourusername/book-destiny.git
cd book-destiny

Install the required dependencies:
pip install -r requirements.txt

Setup the database:
python manage.py migrate

Create a superuser to manage the site:
python manage.py createsuperuser

Run the development server:
python manage.py runserver
Access the project: Open your web browser and go to http://127.0.0.1:8000/.

Usage
User Registration: Register as a new user and activate your account via the email link.
Browse Books: Explore the comprehensive catalog of books, search by title, and view availability.
Borrow Books: Check out available books, reducing their quantity in the library.
Return Books: Return borrowed books, leave a review, and see the quantity updated.
Manage Wishlist: Add books to your wishlist for easy access in your profile.
Technologies Used
Frontend: HTML, CSS, Bootstrap
Backend: Django (Python)
Database: SQLite (or specify the database you used)
Deployment: Deployed on [Your Hosting Platform] (e.g.,render, Heroku, AWS, etc.)
Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.



Acknowledgements
Special thanks to my professors and peers for their support and guidance.
Inspired by real-world library management systems and user feedback.
