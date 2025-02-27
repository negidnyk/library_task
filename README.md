To set up the project:
1. Pull the project
2. Run command: "pip install -r requirements.txt"
3. Wait until packages are installed
4. Set up .env file with DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS, AUTH_SECRET, RESET_PASS_SECRET variables
5. Run command "alembic upgrade head" for applying DB migration: 30d7458d17bd_init_migration.py
6. Go to the any PostgresSQL management tool (PGAdmin, for example)
7. Connect to the DB with your own creds which you used for DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
8. Make sure that "alembic_version" table contains valid version (30d7458d17bd)
9. Make sure that tables: roles, users, books, authors, genres, publishers, borrowed_books are crated
10. Make sure that table 'roles' contains 2 roles: librarian with id 1 and borrower with id 2
11. Run command: "uvicorn main:app --reload"
12. Go to the path: "http://127.0.0.1:8000/docs#/" in a browser
13. Interact with a Swagger

Information about authentication:
Authentication is based on Bearer tokens
There 3 APIs in swagger:
1. /auth/jwt/login
2. /auth/jwt/logout
3. /auth/jwt/register
    
To interract with swagger you have to be autenticated, so you can use "/auth/jwt/register" endpoint to create a user with data like this: 
{
  "email": "testemail@gmail.com",
  "password": "Qwerty12#",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false,
  "username": "Test User",
  "role_id": 1, // 1 is librarian role, 2 is borrower (there are restrictions added for using endpoints according to role of user)
  "is_deleted": false
}

Then you should use "/auth/jwt/login" endpint to log in. You should submit username (actually, it`s email. Funny tricks of fastapi-users lib) and password to be signed in. According to the data for creating a user, email and password is:
email: testemail@gmail.com
password: Qwerty12#
In response, you will receive a Bearer token. Use as "Authorization" header in each request.

Also, the most suitable way to be signed in is just to clik on any icon of "lock" in a Swagger, submit email and password of created user and thats all.

"/auth/jwt/logout" endping does nothing, because of specifics of Bearer token

Restrictions of endpints by role:
1. POST "/authors/add/" - is available for users with role_id == 1 (librarians)
2. POST "/books/add/" - is available for users with role_id == 1 (librarians)
3. DELETE "/books/{book_id}/" - is available for users with role_id == 1 (librarians)
4. POST "/books/borrow/{book_id}/" - is available for users with role_id == 2 (borrowers)
5. POST "/books/return/{book_id}/" - is available for users with role_id == 2 (borrowers)
6. GET "/books/{book_id}/history/" - is available for users with role_id == 1 (librarians)
7. POST "/genres/add/" - is available for users with role_id == 1 (librarians)
8. POST "/publishers/add/" - is available for users with role_id == 1 (librarians)

Validations of endpints:
1. POST "/authors/add/": name should be unique, date should be in the past
2. POST "/books/add/": isbn should be unique, author, genre, publisher should exist in db, publish_date should be in the past
3. DELETE "/books/{book_id}/": book with submitted id should exist in DB
4. POST "/books/borrow/{book_id}/": user, who borrows, should has an id == 2 (borrower), book with submitted id should exist in DB, book with submitted id should not be borrowed yet (is_borrowed == False)
5. POST "/books/return/{book_id}/": user, who returns, should has an id == 2 (borrower), book with submitted id should exist in DB, user should have a record of borrowing specified book in borrowed_books table with empty return_date, book with submitted id should exist in DB should be borrowed (is_borrowed == True)
6. GET "/books/{book_id}/history/" - is available for users with role_id == 1 (librarians), book with submitted id should exist in DB
7. POST "/genres/add/" - is available for users with role_id == 1 (librarians), genre name should be unique
8. POST "/publishers/add/" - is available for users with role_id == 1 (librarians), publisher name should be unique



    
    

