import csv
from items_and_containers import Item, load_items

# Define the Compartment class for multi-compartment containers
class Compartment:
    def __init__(self, name, empty_weight, weight_capacity):
        self.name = name
        self.empty_weight = empty_weight
        self.weight_capacity = weight_capacity
        self.items = []
        self.current_weight = 0

    def add_item(self, item):
        if self.current_weight + item.weight <= self.weight_capacity:
            self.items.append(item)
            self.current_weight += item.weight
            return True
        return False

    def __str__(self):
        items_str = "\n   ".join([str(item) for item in self.items])
        return (f"{self.name} (total weight: {self.empty_weight + self.current_weight}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_weight}/{self.weight_capacity})\n   {items_str}")

# Define the Container class
class Container:
    def __init__(self, name, empty_weight, capacity):
        self.name = name
        self.empty_weight = empty_weight
        self.capacity = capacity
        self.current_weight = 0
        self.loot = []

    def add_item(self, item):
        if self.current_weight + item.weight <= self.capacity:
            self.loot.append(item)
            self.current_weight += item.weight
            return True
        return False

    def __str__(self):
        items_str = "\n   ".join([str(item) for item in self.loot])
        return (f"{self.name} (total weight: {self.empty_weight + self.current_weight}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_weight}/{self.capacity})\n   {items_str}")

# Define the MagicContainer class, which inherits from Container
class MagicContainer(Container):
    def add_item(self, item):
        if self.current_weight + item.weight <= self.capacity:
            self.loot.append(item)
            self.current_weight += item.weight
            return True
        return False

    def __str__(self):
        items_str = "\n   ".join([str(item) for item in self.loot])
        return (f"{self.name} (total weight: {self.empty_weight}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_weight}/{self.capacity})\n   {items_str}")

# Function to load magic containers based on the 'Container' column in magic_containers.csv
def load_magic_containers(filename):
    magic_containers = set()
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        # Strip spaces from field names to handle headers with extra spaces
        reader.fieldnames = [header.strip() for header in reader.fieldnames]

        for row in reader:
            # Load the container name from the 'Container' column, now guaranteed to be space-free
            magic_containers.add(row['Container'].strip())
    print("Magic Containers Loaded:", magic_containers)  # Debug statement
    return magic_containers

# Function to load containers based on type (single, multi, magic)
def load_containers(filename, magic_containers):
    containers = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name'].strip()
            empty_weight = int(row[' Empty Weight'].strip())
            capacity = int(row[' Weight Capacity'].strip())
            
            if name in magic_containers:
                container = MagicContainer(name, empty_weight, capacity)
                print(f"Loaded MagicContainer: {name}")  # Debug statement
            else:
                container = Container(name, empty_weight, capacity)
                print(f"Loaded Container: {name}")  # Debug statement
            containers.append(container)
    return containers

# Function to initialize items and containers
def initialize_game_data():
    items = load_items('data/items.csv')
    magic_containers = load_magic_containers('data/magic_containers.csv')
    containers = load_containers('data/containers.csv', magic_containers)
    print("="*50)
    print(f"Initialized {len(items) + len(containers)} items including {len(containers)} containers.")
    return items, containers

# Main game loop for looting system
def main():
    items, containers = initialize_game_data()
    container_name = input("Enter the name of the container: ").strip()
    selected_container = next((c for c in containers if c.name == container_name), None)
    
    if not selected_container:
        print(f'"{container_name}" not found. Exiting...')
        return

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
            item_to_loot = next((i for i in items if i.name == item_name), None)
            
            if item_to_loot:
                if selected_container.add_item(item_to_loot):
                    print(f'Success! Item "{item_to_loot.name}" stored in container "{selected_container.name}".')
                else:
                    print(f'Failure! Item "{item_to_loot.name}" NOT stored in container "{selected_container.name}".')
            else:
                print(f'"{item_name}" not found. Try again.')

        elif choice == "2":
            print(f"\n{selected_container}")
        
        elif choice == "0":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()