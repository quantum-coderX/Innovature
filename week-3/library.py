import csv
import os
from book import Book
from member import Member
from transaction import Transaction
from datetime import datetime

class Library:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.books_file = os.path.join(data_dir, 'books.csv')
        self.members_file = os.path.join(data_dir, 'members.csv')
        self.transactions_file = os.path.join(data_dir, 'transactions.csv')
        self.books = []
        self.members = []
        self.transactions = []
        self.load_data()

    def load_data(self):
        try:
            with open(self.books_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    book = Book(
                        int(row['book_id']),
                        row['title'],
                        row['author'],
                        row['isbn'],
                        row['available'].lower() == 'true'
                    )
                    self.books.append(book)
        except FileNotFoundError:
            pass
        except (ValueError, KeyError) as e:
            raise ValueError(f"Error loading books CSV: {e}")

        try:
            with open(self.members_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    member = Member(
                        int(row['member_id']),
                        row['name'],
                        row['email']
                    )
                    self.members.append(member)
        except FileNotFoundError:
            pass
        except (ValueError, KeyError) as e:
            raise ValueError(f"Error loading members CSV: {e}")

        try:
            with open(self.transactions_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    transaction = Transaction(
                        int(row['transaction_id']),
                        int(row['book_id']),
                        int(row['member_id']),
                        row['borrow_date'],
                        row['due_date'],
                        row['return_date'] if row['return_date'] else None,
                        float(row['late_fee'])
                    )
                    self.transactions.append(transaction)
        except FileNotFoundError:
            pass
        except (ValueError, KeyError) as e:
            raise ValueError(f"Error loading transactions CSV: {e}")

    def save_data(self):
        try:
            with open(self.books_file, 'w', newline='') as f:
                if self.books:
                    writer = csv.DictWriter(f, fieldnames=self.books[0].to_dict().keys())
                    writer.writeheader()
                    for book in self.books:
                        writer.writerow(book.to_dict())
        except IOError as e:
            raise IOError(f"Error saving books CSV: {e}")

        try:
            with open(self.members_file, 'w', newline='') as f:
                if self.members:
                    writer = csv.DictWriter(f, fieldnames=self.members[0].to_dict().keys())
                    writer.writeheader()
                    for member in self.members:
                        writer.writerow(member.to_dict())
        except IOError as e:
            raise IOError(f"Error saving members CSV: {e}")

        try:
            with open(self.transactions_file, 'w', newline='') as f:
                if self.transactions:
                    writer = csv.DictWriter(f, fieldnames=self.transactions[0].to_dict().keys())
                    writer.writeheader()
                    for transaction in self.transactions:
                        writer.writerow(transaction.to_dict())
        except IOError as e:
            raise IOError(f"Error saving transactions CSV: {e}")

    def add_book(self, book):
        if any(b.book_id == book.book_id for b in self.books):
            raise ValueError(f"Book with ID {book.book_id} already exists")
        self.books.append(book)
        self.save_data()
        print(f"Book '{book.title}' added successfully.")

    def add_member(self, member):
        if any(m.member_id == member.member_id for m in self.members):
            raise ValueError(f"Member with ID {member.member_id} already exists")
        self.members.append(member)
        self.save_data()
        print(f"Member '{member.name}' added successfully.")

    def borrow_book(self, book_id, member_id):
        book = next((b for b in self.books if b.book_id == book_id), None)
        if not book:
            raise ValueError(f"Book with ID {book_id} not found")
        if not book.available:
            raise ValueError(f"Book '{book.title}' is not available")

        member = next((m for m in self.members if m.member_id == member_id), None)
        if not member:
            raise ValueError(f"Member with ID {member_id} not found")

        transaction_id = max([t.transaction_id for t in self.transactions], default=0) + 1
        borrow_date = datetime.now()
        transaction = Transaction(transaction_id, book_id, member_id, borrow_date)
        self.transactions.append(transaction)
        book.available = False
        self.save_data()
        print(f"Book '{book.title}' borrowed by {member.name}. Due date: {transaction.due_date.date()}")

    def return_book(self, transaction_id):
        transaction = next((t for t in self.transactions if t.transaction_id == transaction_id and t.return_date is None), None)
        if not transaction:
            raise ValueError(f"Active transaction with ID {transaction_id} not found")

        return_date = datetime.now()
        late_fee = transaction.calculate_late_fee(return_date)
        transaction.return_date = return_date

        book = next((b for b in self.books if b.book_id == transaction.book_id), None)
        if book:
            book.available = True

        self.save_data()
        print(f"Book returned. Late fee: ${late_fee:.2f}")