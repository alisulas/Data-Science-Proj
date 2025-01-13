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
        self.items = []  # To store items, if needed in future tasks

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


# Function to display all items
def display_all_items(items):
    print("Items:")
    for item in items:
        print(item)


# Function to display all containers
def display_all_containers(containers):
    print("\nContainers:")
    for container in containers:
        print(container)


# Main code for testing Task 4
if __name__ == "__main__":
    # Load items and containers from CSV files
    items = load_items("data/items.csv")
    containers = load_containers("data/containers.csv")
    
    # Display loaded items and containers
    display_all_items(items)
    display_all_containers(containers)
