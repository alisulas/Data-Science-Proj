# Task 8: Magic Multi-Compartment Containers

# Logic Comment
# 1. Load items, single-compartment, multi-compartment, magic, and magic multi-compartment containers from CSV files.
# 2. Ask user to select any container for adventure.
# 3. Display menu with options to loot items or list looted items.

# 4. Loot item:
#    - Get item name, place in first compartment with enough capacity.
#    - For magic multi-compartment containers, add item without increasing compartment weight.
#    - Show success if stored; show failure if no compartments have enough space.

# 5. List looted items:
#    - Display container details with empty weight, capacity, and each compartment’s items.
#    - For magic multi-compartment containers, show compartment contents and remaining capacity without adding item weights.

# 6. Loop menu until user chooses to quit.

# Key Difference from Task 7:
# - Magic multi-compartment containers allow multiple independent compartments that ignore item weights.
# - Capacity constraints are per compartment, but added items do not increase compartment weight.
# - Display output includes each compartment's capacity without reflecting item weights.

# Hermione's Satchel Professor Farnsworth's Lab Coat

import csv

# Define the Item class
class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __str__(self):
        return f"{self.name} (weight: {self.weight})"

# Define the base Compartment class
class Compartment:
    def __init__(self, name, empty_weight, capacity):
        self.name = name
        self.empty_weight = empty_weight
        self.capacity = capacity
        self.current_weight = 0
        self.items = []

    def can_add_item(self, item):
        return self.current_weight + item.weight <= self.capacity

    def add_item(self, item):
        if self.can_add_item(item):
            self.items.append(item)
            self.current_weight += item.weight
            return True
        return False

    def __str__(self):
        items_str = "\n     ".join([str(item) for item in self.items])
        return (f"{self.name} (total weight: {self.empty_weight + self.current_weight}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_weight}/{self.capacity})\n     {items_str}")

# Define the MagicCompartment class that respects capacity but not weight
class MagicCompartment(Compartment):
    def add_item(self, item):
        if self.current_weight + item.weight <= self.capacity:
            self.items.append(item)
            # Capacity affects storage, but weight does not change
            return True
        return False

    def __str__(self):
        items_str = "\n     ".join([str(item) for item in self.items])
        return (f"{self.name} (total weight: {self.empty_weight}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_weight}/{self.capacity})\n     {items_str}")

# Define the MagicMultiContainer for containers with multiple magic compartments
class MagicMultiContainer:
    def __init__(self, name):
        self.name = name
        self.compartments = []
        self.empty_weight = 0

    def add_compartment(self, compartment):
        self.compartments.append(compartment)
        self.empty_weight += compartment.empty_weight

    def add_item(self, item):
        for compartment in self.compartments:
            if compartment.add_item(item):
                return True
        return False

    def __str__(self):
        compartments_str = "\n     ".join([str(compartment) for compartment in self.compartments])
        return f"{self.name} (total weight: {self.empty_weight}, empty weight: {self.empty_weight}, capacity: 0/0)\n     {compartments_str}"

# Load items from CSV
def load_items(filename):
    items = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = Item(row['Name'].strip(), int(row[' Weight'].strip()))
            items.append(item)
    return items

# Load compartments data
def load_compartments_data(filename):
    compartments = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name'].strip()
            empty_weight = int(row[' Empty Weight'].strip())
            capacity = int(row[' Weight Capacity'].strip())
            compartments[name] = (empty_weight, capacity)
    return compartments

# Load magic multi-compartment containers
def load_magic_multi_containers(filename, compartments_data):
    containers = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            container_name = row[0].strip()
            compartment_names = [compartment.strip() for compartment in row[1:]]
            magic_container = MagicMultiContainer(container_name)
            for name in compartment_names:
                empty_weight, capacity = compartments_data.get(name, (1, 1000))
                compartment = MagicCompartment(name, empty_weight, capacity)
                magic_container.add_compartment(compartment)
            containers.append(magic_container)
    return containers

# Select container
def select_container(all_containers):
    while True:
        container_name = input("Enter the name of the container: ").strip()
        for container in all_containers:
            if container.name.lower() == container_name.lower():
                return container
        print(f'"{container_name}" not found. Try again.')

# Main menu
def main_menu(container, items):
    while True:
        print("\n==================================")
        print("Enter your choice:")
        print("1. Loot item.")
        print("2. List looted items.")
        print("0. Quit.")
        print("==================================")
        
        choice = input("Your choice: ").strip()
        
        if choice == "1":
            item_name = input("Enter the name of the item: ").strip()
            item = next((i for i in items if i.name.lower() == item_name.lower()), None)
            if not item:
                print(f'"{item_name}" not found. Try again.')
            elif container.add_item(item):
                print(f'Success! Item "{item_name}" stored in container "{container.name}".')
            else:
                print(f'Failure! Item "{item_name}" NOT stored in container "{container.name}".')
        
        elif choice == "2":
            print(f"\n{container}")
        
        elif choice == "0":
            print("Exiting the game.")
            break
        else:
            print("Invalid choice. Please try again.")

# Main program
def main():
    items = load_items('data/items.csv')
    compartments_data = load_compartments_data('data/containers.csv')
    magic_multi_containers = load_magic_multi_containers('data/magic_multi_containers.csv', compartments_data)
    
    # Combine container types, if necessary (e.g., magic, single, etc.)
    all_containers = magic_multi_containers  # Add other container types as needed

    # Initialization message
    print(f"Initialized {len(items)} items including {len(all_containers)} containers.")
    
    selected_container = select_container(all_containers)
    main_menu(selected_container, items)

if __name__ == "__main__":
    main()
