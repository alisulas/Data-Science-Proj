from table_menu_duplicate import tables, list_tables, display_table, duplicate_table  # Import Task 1 functions
from tabulate import tabulate

# Task 2 Functions: Create and Delete Table
def create_table():
    print("Available tables:")
    for i, (header, _) in enumerate(tables):
        print(f"{i}: {header}")
    while True:
        try:
            index = int(input("Choose a table index (to create from): "))
            if 0 <= index < len(tables):
                header, data = tables[index]
                break
            else:
                print("Incorrect table index. Try again.")
        except ValueError:
            print("Please enter a valid number.")
    print("Columns available in the selected table:")
    for i, col_name in enumerate(header):
        print(f"{i}: {col_name}")
    while True:
        try:
            col_indices = input("Enter the comma-separated indices of the columns to keep: ").split(',')
            col_indices = [int(i.strip()) for i in col_indices]
            if all(0 <= i < len(header) for i in col_indices):
                new_header = [header[i] for i in col_indices]
                new_data = [[row[i] for i in col_indices] for row in data]
                tables.append((new_header, new_data))
                print("New table created successfully.")
                break
            else:
                print("Some indices are out of range. Try again.")
        except ValueError:
            print("Please enter comma-separated numbers only.")

def delete_table():
    print("Available tables:")
    for i, (header, _) in enumerate(tables):
        print(f"{i}: {header}")
    while True:
        try:
            index = int(input("Choose a table index (to delete): "))
            if 0 <= index < len(tables):
                tables.pop(index)
                print(f"Table {index} deleted successfully.")
                break
            else:
                print("Incorrect table index. Try again.")
        except ValueError:
            print("Please enter a valid number.")

# Main menu for Task 2
def main_menu():
    while True:
        print("="*43)
        print("Main Menu - Task 2")
        print("1. List tables")
        print("2. Display table")
        print("3. Duplicate table")
        print("4. Create a new table from an existing table")
        print("5. Delete a table")
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
        elif choice == "0":
            print("Exiting Task 2.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main menu
if __name__ == "__main__":
    main_menu()