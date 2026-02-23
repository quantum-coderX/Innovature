import argparse
from database import Database

def main():
    parser = argparse.ArgumentParser(description='Student Record Management CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new student')
    add_parser.add_argument('--name', required=True, help='Student name')
    add_parser.add_argument('--grade', required=True, help='Student grade')

    # View command
    subparsers.add_parser('view', help='View all students')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update a student record')
    update_parser.add_argument('--id', type=int, required=True, help='Student ID')
    update_parser.add_argument('--name', required=True, help='New student name')
    update_parser.add_argument('--grade', required=True, help='New student grade')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a student record')
    delete_parser.add_argument('--id', type=int, required=True, help='Student ID')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search students')
    search_parser.add_argument('--type', choices=['name', 'grade', 'id'], required=True, help='Search type')
    search_parser.add_argument('--value', required=True, help='Search value')

    # Export command
    export_parser = subparsers.add_parser('export', help='Export students to CSV')
    export_parser.add_argument('--filename', default='students.csv', help='CSV filename')

    args = parser.parse_args()

    if args.command == 'add':
        db.add_student(args.name, args.grade)
        print('Student added successfully!')
    elif args.command == 'view':
        students = db.get_students()
        if not students:
            print('No students found.')
        else:
            for student in students:
                print(f'{student[0]}: {student[1]} - {student[2]}')
    elif args.command == 'update':
        db.update_student(args.id, args.name, args.grade)
        print('Student updated successfully!')
    elif args.command == 'delete':
        db.delete_student(args.id)
        print('Student deleted successfully!')
    elif args.command == 'search':
        if args.type == 'name':
            students = db.search_by_name(args.value)
        elif args.type == 'grade':
            students = db.search_by_grade(args.value)
        elif args.type == 'id':
            student = db.search_by_id(int(args.value))
            students = [student] if student else []
        if not students:
            print('No students found.')
        else:
            for student in students:
                print(f'{student[0]}: {student[1]} - {student[2]}')
    elif args.command == 'export':
        db.export_to_csv(args.filename)
        print(f'Students exported to {args.filename}')
    else:
        parser.print_help()

if __name__ == '__main__':
    db = Database()
    try:
        main()
    finally:
        db.close()