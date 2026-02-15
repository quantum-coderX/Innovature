from datetime import datetime, timedelta

class Transaction:
    def __init__(self, transaction_id, book_id, member_id, borrow_date, due_date=None, return_date=None, late_fee=0.0):
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.borrow_date = borrow_date if isinstance(borrow_date, datetime) else datetime.fromisoformat(borrow_date)
        self.due_date = due_date if due_date is None else (due_date if isinstance(due_date, datetime) else datetime.fromisoformat(due_date))
        if self.due_date is None:
            self.due_date = self.borrow_date + timedelta(days=14)
        self.return_date = return_date if return_date is None else (return_date if isinstance(return_date, datetime) else datetime.fromisoformat(return_date))
        self.late_fee = late_fee

    def calculate_late_fee(self, return_date, daily_fee=0.5):
        if isinstance(return_date, str):
            return_date = datetime.fromisoformat(return_date)
        if return_date > self.due_date:
            days_late = (return_date - self.due_date).days
            self.late_fee = days_late * daily_fee
        return self.late_fee

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'borrow_date': self.borrow_date.isoformat(),
            'due_date': self.due_date.isoformat(),
            'return_date': self.return_date.isoformat() if self.return_date else '',
            'late_fee': self.late_fee
        }

    def __str__(self):
        return f"Transaction({self.transaction_id}, {self.book_id}, {self.member_id}, {self.borrow_date.date()}, {self.due_date.date()}, {self.return_date.date() if self.return_date else None}, {self.late_fee})"