import argparse
from library import Library
from book import Book
from member import Member

def list_books(library):
    if not library.books:
        print("No books in the library.")
    else:
        print("Books:")
        for book in library.books:
            status = "Available" if book.available else "Borrowed"
            print(f"  ID: {book.book_id}, Title: {book.title}, Author: {book.author}, Status: {status}")

def list_members(library):
    if not library.members:
        print("No members in the library.")
    else:
        print("Members:")
        for member in library.members:
            print(f"  ID: {member.member_id}, Name: {member.name}, Email: {member.email}")

def list_transactions(library):
    if not library.transactions:
        print("No transactions in the library.")
    else:
        print("Transactions:")
        for transaction in library.transactions:
            return_status = f"Returned on {transaction.return_date.date()}" if transaction.return_date else "Not returned"
            print(f"  ID: {transaction.transaction_id}, Book ID: {transaction.book_id}, Member ID: {transaction.member_id}, Due: {transaction.due_date.date()}, {return_status}, Late Fee: ${transaction.late_fee:.2f}")

def interactive_mode():
    library = Library()
    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Add Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. List Books")
        print("6. List Members")
        print("7. List Transactions")
        print("8. Exit")
        choice = input("Choose an option (1-8): ").strip()

        try:
            if choice == '1':
                book_id = int(input("Book ID: "))
                title = input("Title: ")
                author = input("Author: ")
                isbn = input("ISBN: ")
                book = Book(book_id, title, author, isbn)
                library.add_book(book)
            elif choice == '2':
                member_id = int(input("Member ID: "))
                name = input("Name: ")
                email = input("Email: ")
                member = Member(member_id, name, email)
                library.add_member(member)
            elif choice == '3':
                book_id = int(input("Book ID: "))
                member_id = int(input("Member ID: "))
                library.borrow_book(book_id, member_id)
            elif choice == '4':
                transaction_id = int(input("Transaction ID: "))
                library.return_book(transaction_id)
            elif choice == '5':
                list_books(library)
            elif choice == '6':
                list_members(library)
            elif choice == '7':
                list_transactions(library)
            elif choice == '8':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Library Management CLI')
    subparsers = parser.add_subparsers(dest='command')

    add_book_parser = subparsers.add_parser('add-book')
    add_book_parser.add_argument('book_id', type=int, help='Unique book ID')
    add_book_parser.add_argument('title', help='Book title')
    add_book_parser.add_argument('author', help='Book author')
    add_book_parser.add_argument('isbn', help='Book ISBN')

    add_member_parser = subparsers.add_parser('add-member')
    add_member_parser.add_argument('member_id', type=int, help='Unique member ID')
    add_member_parser.add_argument('name', help='Member name')
    add_member_parser.add_argument('email', help='Member email')

    borrow_parser = subparsers.add_parser('borrow')
    borrow_parser.add_argument('book_id', type=int, help='Book ID to borrow')
    borrow_parser.add_argument('member_id', type=int, help='Member ID borrowing the book')

    return_parser = subparsers.add_parser('return')
    return_parser.add_argument('transaction_id', type=int, help='Transaction ID to return')

    list_books_parser = subparsers.add_parser('list-books')

    list_members_parser = subparsers.add_parser('list-members')

    list_transactions_parser = subparsers.add_parser('list-transactions')

    args = parser.parse_args()

    if args.command is None:
        interactive_mode()
        return

    try:
        library = Library()
        if args.command == 'add-book':
            book = Book(args.book_id, args.title, args.author, args.isbn)
            library.add_book(book)
        elif args.command == 'add-member':
            member = Member(args.member_id, args.name, args.email)
            library.add_member(member)
        elif args.command == 'borrow':
            library.borrow_book(args.book_id, args.member_id)
        elif args.command == 'return':
            library.return_book(args.transaction_id)
        elif args.command == 'list-books':
            list_books(library)
        elif args.command == 'list-members':
            list_members(library)
        elif args.command == 'list-transactions':
            list_transactions(library)
        else:
            parser.print_help()
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()