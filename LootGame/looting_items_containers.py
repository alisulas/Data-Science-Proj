import csv

# Define the Item class
class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight

    def __str__(self):
        return f"{self.name} (weight: {self.weight})"


# Define the Container class
class Container:
    def __init__(self, name, empty_weight, capacity):
        self.name = name
        self.empty_weight = empty_weight
        self.capacity = capacity
        self.items = []  # List to store looted items

    def add_item(self, item):
        total_weight = self.empty_weight + sum(i.weight for i in self.items) + item.weight
        if total_weight <= self.capacity:
            self.items.append(item)
            return f"Success! Item '{item.name}' stored in container '{self.name}'."
        else:
            return f"Failure! Item '{item.name}' NOT stored in container '{self.name}'."

    def list_looted_items(self):
        item_list = "\n   ".join(str(item) for item in self.items)
        return f"{self.name} (total weight: {self.empty_weight + sum(i.weight for i in self.items)}, empty weight: {self.empty_weight}, capacity: {sum(i.weight for i in self.items)}/{self.capacity})\n   {item_list}"

    def __str__(self):
        return f"{self.name} (total weight: {self.empty_weight}, empty weight: {self.empty_weight}, capacity: 0/{self.capacity})"


# Function to load items from items.csv
def load_items(filepath):
    items = []
    try:
        with open(filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Name']
                weight = int(row[' Weight'])
                items.append(Item(name, weight))
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    return items


# Function to load containers from containers.csv
def load_containers(filepath):
    containers = []
    try:
        with open(filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Name']
                empty_weight = int(row[' Empty Weight'])
                capacity = int(row[' Weight Capacity'])
                containers.append(Container(name, empty_weight, capacity))
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    return containers


# Function to select a container by name
def select_container(containers, container_name):
    for container in containers:
        if container.name == container_name:
            return container
    return None


# Function to loot an item by name
def loot_item(container, items, item_name):
    for item in items:
        if item.name == item_name:
            return container.add_item(item)
    return f"'{item_name}' not found. Try again."


# Function to display all looted items in the selected container
def display_looted_items(container):
    print(container.list_looted_items())


# Main code for testing Task 5
if __name__ == "__main__":
    # Load items and containers from CSV files
    items = load_items("data/items.csv")
    containers = load_containers("data/containers.csv")

    # Prompt user to select a container, retry until valid
    selected_container = None
    while selected_container is None:
        container_name = input("Enter the name of the container: ")
        selected_container = select_container(containers, container_name)
        if selected_container is None:
            print(f"'{container_name}' not found. Try again.")

    # Proceed to looting items once a valid container is selected
    while True:
        print("\n==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")
        choice = input("Choice: ")

        if choice == '1':
            item_name = input("Enter the name of the item: ")
            result = loot_item(selected_container, items, item_name)
            print(result)

        elif choice == '2':
            display_looted_items(selected_container)

        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
