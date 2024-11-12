from table_menu_duplicate import tables, list_tables, display_table, duplicate_table  # Import Task 1 functions
from table_menu_create_delete import create_table, delete_table  # Import Task 2 functions
from tabulate import tabulate

# Deleted tables storage for restoration
deleted_tables = {}

# Task 3 Functions: Delete Column and Restore Table
def delete_column():
    while True:
        try:
            table_index = int(input("Choose a table index (for column deletion): "))
            if 0 <= table_index < len(tables):
                header, data = tables[table_index]
                print("Columns available in the selected table: ")
                for i, col_name in enumerate(header):
                    print(f"{i}: {col_name}")
                column_index = int(input("Enter the index of the column to delete: "))
                if 0 <= column_index < len(header):
                    new_header = header[:column_index] + header[column_index + 1:]
                    new_data = [row[: column_index] + row[column_index + 1:] for row in data]
                    tables[table_index] = (new_header, new_data)
                    print(f"Column {column_index} deleted successfully.")
                    break
                else:
                    print("Incorrect column index. Try again.")
            else:
                print("Incorrect table index. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def restore_table():
    if not deleted_tables:
        print("No tables are currently available for restoration.")
        return
    while True:
        try:
            index = int(input("Choose a table index (for restoration): "))
            if index in deleted_tables:
                tables.insert(index, deleted_tables.pop(index))
                print(f"Table {index} has been restored.")
                break
            else:
                print("Incorrect table index. Try again.")
        except ValueError:
            print("Please enter a valid number.")

# Main menu for Task 3
def main_menu():
    while True:
        print("="*43)
        print("Main Menu - Task 3")
        print("1. List tables")
        print("2. Display table")
        print("3. Duplicate table")
        print("4. Create a new table from an existing table")
        print("5. Delete a table")
        print("6. Delete column from a table")
        print("7. Restore a deleted table")
        print("0. Quit")
        print("="*43)
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            list_tables()
        elif choice == "2":
            display_table()
        elif choice == "3":
            duplicate_table()
        elif choice == "4":
            create_table()
        elif choice == "5":
            delete_table()
        elif choice == "6":
            delete_column()
        elif choice == "7":
            restore_table()
        elif choice == "0":
            print("Exiting Task 3.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main menu
if __name__ == "__main__":
    main_menu()