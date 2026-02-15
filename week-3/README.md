# Library Management CLI Tool

A comprehensive command-line application for managing a library system, built with Python. The tool allows librarians and users to manage books, members, and borrowing transactions with automatic late fee calculations.

## Features

- **Book Management**: Add, list, and track book availability
- **Member Management**: Register and manage library members
- **Borrowing System**: Handle book checkouts with due dates
- **Return Processing**: Process book returns with automatic late fee calculation
- **Data Persistence**: All data stored in CSV files with error handling
- **Dual Interface**: Both interactive menu and command-line modes
- **Input Validation**: Comprehensive error handling and validation

## Architecture

### Core Classes

- **`Book`**: Represents a book with ID, title, author, ISBN, and availability status
- **`Member`**: Represents a library member with ID, name, and email
- **`Transaction`**: Manages borrowing records with due dates and late fee calculations

### Data Storage

All data is persisted in CSV files located in the `data/` directory:
- `books.csv`: Book inventory
- `members.csv`: Member registry
- `transactions.csv`: Borrowing history

### CLI Structure

```
main.py (entry point)
├── cli.py (command-line interface)
│   ├── interactive_mode() - Menu-driven interface
│   └── Argument parsing with subcommands
└── library.py (business logic)
    ├── Book/Member/Transaction management
    └── CSV data persistence
```

## How It Works

### Data Flow
1. **Initialization**: Program loads existing data from CSV files on startup
2. **Operations**: User performs actions through CLI (add, borrow, return, list)
3. **Validation**: Input validation and business rule enforcement
4. **Persistence**: Changes automatically saved to CSV files
5. **Feedback**: User receives confirmation and status updates

### Key Logic

- **Borrowing**: Creates transaction with 14-day due date, marks book unavailable
- **Returning**: Calculates late fees ($0.50/day), updates book availability
- **Late Fees**: Automatically computed based on days past due date
- **ID Management**: Auto-generates transaction IDs, validates uniqueness

## Installation & Setup

### Prerequisites
- Python 3.6+
- No external dependencies required

### Setup
1. Navigate to the project directory:
   ```bash
   cd week-3
   ```

2. Ensure data directory exists (auto-created on first run):
   ```bash
   mkdir data  # Usually not needed as it's created automatically
   ```

## Usage

### Interactive Mode (Default)
Run the program without arguments for a user-friendly menu:

```bash
python main.py
```

This launches an interactive menu where you can:
- Add books and members
- Borrow and return books
- View all records
- Exit the program

### Command-Line Mode
Use specific subcommands for automation and scripting:

```bash
# Add a book
python main.py add-book <id> "<title>" "<author>" "<isbn>"

# Add a member
python main.py add-member <id> "<name>" "<email>"

# Borrow a book
python main.py borrow <book_id> <member_id>

# Return a book
python main.py return <transaction_id>

# List records
python main.py list-books
python main.py list-members
python main.py list-transactions
```

## Examples

### Complete Workflow

```bash
# Start interactive mode
python main.py

# Or use command-line for automation
python main.py add-book 1 "1984" "George Orwell" "978-0451524935"
python main.py add-member 1 "Alice Johnson" "alice@email.com"
python main.py borrow 1 1
python main.py list-transactions
# (After 14+ days...)
python main.py return 1
```

### Sample Output

```
$ python main.py add-book 1 "The Great Gatsby" "F. Scott Fitzgerald" "978-0-7432-7356-5"
Book 'The Great Gatsby' added successfully.

$ python main.py borrow 1 1
Book 'The Great Gatsby' borrowed by John Doe. Due date: 2026-03-01

$ python main.py return 1
Book returned. Late fee: $2.50
```

## Error Handling

The application includes comprehensive error handling:

- **File I/O Errors**: Graceful handling of CSV read/write issues
- **Invalid Input**: Validation for IDs, dates, and required fields
- **Business Rules**: Prevents borrowing unavailable books, duplicate IDs
- **Data Integrity**: Ensures CSV files remain consistent

## Data Files

### books.csv
```csv
book_id,title,author,isbn,available
1,"The Great Gatsby","F. Scott Fitzgerald","978-0-7432-7356-5",false
```

### members.csv
```csv
member_id,name,email
1,"John Doe","john@example.com"
```

### transactions.csv
```csv
transaction_id,book_id,member_id,borrow_date,due_date,return_date,late_fee
1,1,1,2026-02-15,2026-03-01,2026-03-05,2.5
```

## Development Notes

- **CSV Format**: Uses standard CSV with headers for data portability
- **Date Handling**: ISO format dates (YYYY-MM-DD) for consistency
- **ID Generation**: Transaction IDs auto-increment from existing records
- **Memory Management**: All data loaded into memory for fast operations
- **Thread Safety**: Single-threaded design, not suitable for concurrent access
