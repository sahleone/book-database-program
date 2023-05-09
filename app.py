# import models
from models import (
    Base,
    session,
    Book,
    engine
)
import
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
            \r5) Exit
            """
        )

        choice = input("Which option would you like: ")
        if choice in ["1", "2", "3", "4", "5"]:
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

def add_book():
    # Add a book to the database
    ## Get user input
    title = input("\nPlease enter the title of the book: ")
    author = input("\nPlease enter the author of the book: ")
    published_date = input("\nPlease enter the date of the book (yyyy/mm/dd): ")
    price = input("\nPlease enter the price of the book(10, 5.99): ")

    ## Validate user input
    ### Date
    while True:
        try:
            published_date = datetime.datetime.strptime(published_date, "%Y/%m/%d").date()
            break
        except ValueError:
            print("\nIncorrect date format, please try again")
            print("To abort adding a book, enter 'q'")
            published_date = input("\nPlease enter the date of the book (yyyy/mm/dd): ")
            if published_date.lower() == "q":
                break

    ### Price
    while True:
        try:
            price = float(price)
            break
        except ValueError:
            print("\nIncorrect price format (10, 5.99), please try again")
            print("To abort adding a book, enter 'q'")
            price = input("\nPlease enter the price of the book(10, 5.99): ")
            if price.lower() == "q":
                break

    ## Add book to database
    new_book = Book(title = title, author = author, published_date = published_date, price = price)
    session.add(new_book)

    if session.query(Book).filter(Book.title == title, Book.author == author).one_or_none() is None:
        session.commit()
        print("\nBook added successfully!")
        time.sleep(1.5)

def app():
    app_running = True

    while app_running:
        choice = menu()
        if choice == "1":
            add_book()

        elif choice == "2":
            # view_books()
            continue
        elif choice == "3":
            # search_books()
            continue
        elif choice == "4":
            # analysis_books()
            continue
        else:
            print("\nClosing the application...")
            app_running = False




if __name__=="__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

    for book in session.query(Book):
        print(book)

    print(session.query(Book).count())