# import models
from models import (
    Base,
    session,
    Book,
    engine
)
import time
import datetime
import pandas as pd

def menu():
    while True:
        print(
            """
            \nThe Library!
            \rProgramming Books:
            \r1) Add a book
            \r2) View all books
            \r3) Search for a book
            \r4) Book Analysis
            \r5) Change a book
            \r6) Exit
            """
        )

        choice = input("Which option would you like: ")
        if choice in ["1", "2", "3", "4", "5","6"]:
            return choice
        else:
            print("\nPlease choose one of the options above")
            continue

def menu_search():
    while True:
        print(
            """
            \nSearching Options!
            \r1) By Author Exact
            \r2) By Author Fuzzy
            \r3) By Title Exact
            \r4) By Title Fuzzy
            """
        )

        choice = input("Which option would you like: ")
        if choice in ["1", "2", "3", "4"]:
            return choice
        else:
            print("\nPlease choose one of the options above")
            continue


def menu_update():
    while True:
        print(
            """
            \nChange Options!
            \r1) Update
            \r2) Delete
            \r3) Return to Main Menu
            """
        )

        choice = input("Which option would you like: ")
        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("\nPlease choose one of the options above")
            continue


def  add_csv():
    try:
        df = pd.read_csv("suggested_books.csv",parse_dates=[2],header=None)
        df.columns = ["title", "author", "date", "price"]
        # print(df.head())
    except FileNotFoundError:
        print("File not found, please check the file exists")
        
    for index, row in df.iterrows():
        book_in_db = session.query(Book)\
            .filter(Book.title == row["title"],Book.author == row["author"])\
                .one_or_none()
        if book_in_db is None:
            book = Book(
                title=row["title"],
                author=row["author"],
                published_date= row["date"], #datetime.datetime.strptime(row["date"], "%d/%m/%Y").date(),
                price=row["price"]
            )
            session.add(book)
    session.commit()


def date_check(published_date):
    while True:
        try:
            published_date = datetime.datetime.strptime(published_date, "%Y/%m/%d").date()
            return published_date
        except ValueError:
            print("\nIncorrect date format, please try again")
            print("To abort adding a book, enter 'q'")
            published_date = input("\nPlease enter the date of the book (yyyy/mm/dd): ")
            if published_date.lower() == "q":
                return

    
def price_check(price):
    while True:
        try:
            price = float(price)
            return price
        except ValueError:
            print("\nIncorrect price format (10, 5.99), please try again")
            print("To abort adding a book, enter 'q'")
            price = input("\nPlease enter the price of the book(10, 5.99): ")
            if price.lower() == "q":
                return


def add_book():
    # Add a book to the database
    ## Get user input
    title = input("\nPlease enter the title of the book: ")
    author = input("\nPlease enter the author of the book: ")
    published_date = date_check(input("\nPlease enter the date of the book (yyyy/mm/dd): "))
    # Exit if the date is None
    if published_date is None:
        return

    price = price_check(input("\nPlease enter the price of the book(10, 5.99): "))
    # Exit if the price is None
    if price is None:
        return

    ## Add book to database
    new_book = Book(title = title, author = author, published_date = published_date, price = price)

    if session.query(Book).filter(Book.title == title, Book.author == author,Book.published_date== published_date).one_or_none() is None:
        session.add(new_book)
        session.commit()
        print("\nBook added successfully!")
        time.sleep(1.5)
    else:
        print("\nBook already exists!")
        time.sleep(1.5)

def view_books():
    print("book.id | book.title | book.author | book.price")
    for book in session.query(Book):
        #print(f"{book.id} | {book.title} | {book.author} | {book.price}")
        display_books(book)

    Input = input("\nPress any key to return to the main menu: ")
    if Input:
        return
    


def search_books_author(fuzzy = False):
    # Search for a book
    ## Get user input
    author = input("\nPlease enter the author of the book: ")

    if not fuzzy:
        if not session.query(Book).filter(Book.author == author).first():
            print("\nNo books found")
            time.sleep(1.5)
            return
    else:
        if not session.query(Book).filter(Book.author.like(f"%{author}%")).first():
            print("\nNo books found")
            time.sleep(1.5)
            return
    
    ## Search for book
    if not fuzzy:
        books = session.query(Book)\
            .filter(Book.author == author)
    else:
        books = session.query(Book)\
            .filter(Book.author.like(f"%{author}%"))
            
    ## Display results
    for book in books:
        # print(f"ID: {book.id} Title: {book.title} by {book.author}")
        display_books(book)

    Input = input("\nPress any key to return to the main menu: ")
    if Input:
        return


def search_books_title(fuzzy = False):
    # Search for a book
    ## Get user input
    title = input("\nPlease enter the title of the book: ")

    if not fuzzy:
        if not session.query(Book).filter(Book.title == title).first():
            print("\nNo books found")
            time.sleep(1.5)
            return
    else:
        if not session.query(Book).filter(Book.title.like(f"%{title}%")).first():
            print("\nNo books found")
            time.sleep(1.5)
            return
    
    ## Search for book
    if not fuzzy:
        books = session.query(Book)\
            .filter(Book.title == title)
    else:
        books = session.query(Book)\
            .filter(Book.title.like(f"%{title}%"))
            
    ## Display results
    for book in books:
        print(f"ID: {book.id} Title: {book.title} by {book.author}")

    Input = input("\nPress any key to return to the main menu: ")
    if Input:
        return

def update_book():
    ## Get user input
    bookid= input("\nPlease enter the ID of the book you wish to edit: ")
    
    ids  = session.query(Book.id).all()
    ids = [id[0] for id in ids]
    if int(bookid) in ids:
        bookToUpdate = session.query(Book).filter(Book.id == bookid).first()
    else:
        print("\nNo book found")
        time.sleep(1.5)
        return
    
    # Confirm book to update
    display_books(bookToUpdate)
    confirm = input("\nIs this the book you wish to update? (y/n): ")
    if confirm.lower() == "n":
        return
    
    # Get new values
    print("title | author | published date | price| all")
    value = input("Which value would you like to update?: ")

    if value.lower() == "title":
        bookToUpdate.title = input("\nPlease enter the new title of the book: ")

    elif value.lower() == "author":
        bookToUpdate.author = input("\nPlease enter the new author of the book: ")

    elif value.lower() == "date":
        temp = date_check(input("\nPlease enter the new date of the book (yyyy/mm/dd): "))
        if temp is None:
            return
        else:
            bookToUpdate.published_date = temp

    # Enter price
    elif value.lower() == "price":
        temp = price_check(input("\nPlease enter the new price of the book: "))
        if temp is None:
            return
        else:
            bookToUpdate.price = temp

    # Enter all values
    elif value.lower() == "all":
        bookToUpdate.title = input("\nPlease enter the new title of the book: ")
        bookToUpdate.author = input("\nPlease enter the new author of the book: ")

        # Enter date
        ## Check if the date is valid
        temp = date_check(input("\nPlease enter the new date of the book (yyyy/mm/dd): "))
        if temp is None:
            return
        else:
            bookToUpdate.published_date = temp

        # Enter price
        ## Check if the price is valid
        temp = price_check(input("\nPlease enter the new price of the book: "))
        if temp is None:
            return
        else:
            bookToUpdate.price = temp

    try:
        session.dirty
        session.commit()
        print("\nBook updated successfully!")
    except:
        session.rollback()
        print("Book Change Failed")



def display_books(book):
    print(f"""
            \nID: {book.id} | Title: {book.title} by {book.author}
            \rPublished: {book.published_date} 
            \rPrice: {book.price}
            """)
    


def delete_book():
    ## Get user input
    bookid= input("\nPlease enter the ID of the book you wish to edit: ")
    
    ids  = session.query(Book.id).all()
    ids = [id[0] for id in ids]
    if int(bookid) in ids:
        bookToDelete = session.query(Book).filter(Book.id == bookid).first()
    else:
        print("\nNo book found")
        time.sleep(1.5)
        return
    
    # Confirm book to update
    display_books(bookToDelete)
    confirm = input("\nIs this the book you wish to delete? (y/n): ")
    if confirm.lower() == "n":
        return
    
    try:
        session.delete(bookToDelete)
        session.commit()
        print("\nBook deleted successfully!")
    except:
        session.rollback()
        print("Book Removal Failed")


def app():
    app_running = True

    while app_running:
        choice = menu()
        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            choice_search = menu_search()

            if choice_search == "1":
                search_books_author(fuzzy=False)
            elif choice_search == "2":
                search_books_author(fuzzy=True)
            elif choice_search == "3":
                search_books_title(fuzzy=False)

            elif choice_search == "4":
                search_books_title(fuzzy=True)
      

        elif choice == "4":
            # analysis_books()
            continue
        elif choice == "5":
            choice_update = menu_update()
            if choice_update == "1":
                update_book()

            elif choice_update == "2":
                delete_book()
                
            

        else:
            print("\nClosing the application...")
            app_running = False




if __name__=="__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

    # for book in session.query(Book):
    #     print(book)

    # print(session.query(Book).count())