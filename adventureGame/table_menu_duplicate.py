from tabulate import tabulate

# Define initial tables with headers and data for all 4 tables
header1 = ["Grade Code", "Grade", "Family Grade", "Lower Mark", "Upper Mark"]
data1 = [
    ["HD", "High Distinction", "Hardly Decent", "80", "100"],
    ["D", "Distinction", "Disappointing", "70", "79"],
    ["C", "Credit", "Catastrophic", "60", "69"],
    ["P", "Pass", "Permanent failure", "50", "59"],
    ["N", "Fail", "Never show your face again", "0", "49"]
]

header2 = ["Student ID", "First Name", "Last Name", "Grade Code"]
data2 = [
    ["798154", "Brynhildr", "Blakeley", "N"],
    ["134789", "Felix", "Li", "N"],
    ["798951", "Paityn", "Summers", "P"],
    ["465120", "Turnus", "Elliot", "C"],
    ["963245", "Alysia", "Jervis", "D"],
    ["469120", "Muhammad", "Saad", "HD"]
]

header3 = ["First Name", "Joining Year", "Rabbit"]
data3 = [
    ["Brynhildr", "2022", "Rabbit_1"],
    ["Turnus", "2023", "Rabbit_2"],
    ["Jamaluddin", "2022", "Rabbit_5"]
]

header4 = ["Rabbit", "Birth Year", "Favorite Treat"]
data4 = [
    ["Rabbit_1", "2022", "Carrots"],
    ["Rabbit_2", "2023", "Celery"],
    ["Rabbit_3", "2023", "Broccoli"],
    ["Rabbit_4", "2024", "Cabbage"],
    ["Rabbit_5", "2022", "Lettuce"]
]

# Combine headers and data into the tables list
tables = [
    (header1, data1),
    (header2, data2),
    (header3, data3),
    (header4, data4)
]

# Task 1 Functions: List, Display, Duplicate
def list_tables():
    print("\nIndex    Columns    Rows")
    print("-------  ---------  ------")
    for i, (header, data) in enumerate(tables):
        num_columns = len(header)
        num_rows = len(data)
        print(f"{i:<8} {num_columns:<9} {num_rows}")
    print()

def display_table():
    while True:
        try:
            index = int(input("Choose a table index (to display): "))
            if 0 <= index < len(tables):
                header, data = tables[index]
                print(tabulate(data, headers=header, tablefmt="grid"))
                break
            else:
                print("Incorrect table index. Try again.")
        except ValueError:
            print("Please enter a valid number.")

def duplicate_table():
    while True:
        try:
            index = int(input("Choose a table index (to duplicate): "))
            if 0 <= index < len(tables):
                header, data = tables[index]
                tables.append((header, [row[:] for row in data]))  # Add a copy of the table
                print(f"Table {index} duplicated successfully.")
                break
            else:
                print("Incorrect table index. Try again.")
        except ValueError:
            print("Please enter a valid number.")

# Main menu for Task 1
def main_menu():
    while True:
        print("="*43)
        print("Main Menu - Task 1")
        print("1. List tables")
        print("2. Display table")
        print("3. Duplicate table")
        print("0. Quit")
        print("="*43)
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            list_tables()
        elif choice == "2":
            display_table()
        elif choice == "3":
            duplicate_table()
        elif choice == "0":
            print("Exiting Task 1.")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main menu
if __name__ == "__main__":
    main_menu()