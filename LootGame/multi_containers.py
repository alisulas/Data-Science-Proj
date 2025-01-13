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

    @property
    def total_weight(self):
        # Total weight is the sum of the empty weight and all items' weights
        return self.empty_weight + sum(item.weight for item in self.items)

    def add_item(self, item):
        if self.total_weight + item.weight <= self.capacity:
            self.items.append(item)
            return f"Success! Item '{item.name}' stored in container '{self.name}'."
        else:
            return f"Failure! Item '{item.name}' NOT stored in container '{self.name}'."

    def list_looted_items(self):
        item_list = "\n      ".join(str(item) for item in self.items) if self.items else "None"
        return f"{self.name} (total weight: {self.total_weight}, empty weight: {self.empty_weight}, capacity: {sum(i.weight for i in self.items)}/{self.capacity})\n      {item_list}"

    def __str__(self):
        return f"{self.name} (total weight: {self.total_weight}, empty weight: {self.empty_weight}, capacity: 0/{self.capacity})"


# MultiCompartmentContainer Class inheriting from Container
class MultiCompartmentContainer(Container):
    def __init__(self, name, compartments):
        self.compartments = compartments  # List of Container instances as compartments
        super().__init__(name, self.calculate_empty_weight(), 0)  # Multi-compartment containers have 0 capacity

    def calculate_empty_weight(self):
        # Empty weight is the sum of the empty weights of all compartments
        return sum(compartment.empty_weight for compartment in self.compartments)

    @property
    def total_weight(self):
        # Total weight is the sum of the total weights of all compartments
        return sum(compartment.total_weight for compartment in self.compartments)

    def add_item(self, item):
        # Try adding the item to each compartment until it fits in one of them
        for compartment in self.compartments:
            if compartment.total_weight + item.weight <= compartment.capacity:
                compartment.items.append(item)
                return f"Success! Item '{item.name}' stored in compartment '{compartment.name}' of '{self.name}'."
        return f"Failure! Item '{item.name}' NOT stored in '{self.name}' - no compartment with enough capacity."

    def list_looted_items(self):
        result = f"{self.name} (total weight: {self.total_weight}, empty weight: {self.empty_weight}, capacity: 0/0)"
        for compartment in self.compartments:
            items_str = "\n         ".join(str(item) for item in compartment.items) if compartment.items else "None"
            result += f"\n    {compartment.name} (total weight: {compartment.total_weight}, empty weight: {compartment.empty_weight}, capacity: {sum(i.weight for i in compartment.items)}/{compartment.capacity})\n         {items_str}"
        return result


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


# Function to load multi-compartment containers based on the provided CSV format
def load_multi_compartment_containers(filepath, all_containers):
    multi_containers = []
    try:
        with open(filepath, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                container_name = row['Name']
                
                # Extract compartment names and look them up in the all_containers list
                compartment_names = [name.strip() for name in row[' Containers'].split(',') if name.strip()]
                compartments = [next((c for c in all_containers if c.name == name), None) for name in compartment_names]
                
                # Filter out any None values if a compartment name doesn't match any container in all_containers
                compartments = [comp for comp in compartments if comp is not None]
                
                # Create a MultiCompartmentContainer only if valid compartments are found
                if compartments:
                    multi_containers.append(MultiCompartmentContainer(container_name, compartments))
                    
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    return multi_containers


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


# Main code for testing Task 6
if __name__ == "__main__":
    # Load items, containers, and multi-compartment containers from CSV files
    items = load_items("data/items.csv")
    containers = load_containers("data/containers.csv")
    
    # Combine all standard containers to use as reference for multi-compartment containers
    all_containers = containers.copy()  # Make a copy of standard containers
    
    # Load multi-compartment containers, which reference containers in all_containers
    multi_containers = load_multi_compartment_containers("data/multi_containers.csv", all_containers)
    
    # Add the multi-compartment containers to the all_containers list
    all_containers.extend(multi_containers)
    
    # Prompt user to select a container, retry until valid
    selected_container = None
    while selected_container is None:
        container_name = input("Enter the name of the container: ")
        selected_container = select_container(all_containers, container_name)
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
