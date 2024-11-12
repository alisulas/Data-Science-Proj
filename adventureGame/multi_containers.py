import csv
from items_and_containers import Item, load_items

class Compartment:
    def __init__(self, name, empty_weight, weight_capacity):
        self.name = name
        self.empty_weight = empty_weight
        self.weight_capacity = weight_capacity
        self.items = []
        self.current_weight = 0

    def add_item(self, item):
        #Adds item to compartment if within capacity.#
        if self.current_weight + item.weight <= self.weight_capacity:
            self.items.append(item)
            self.current_weight += item.weight
            return True
        return False

    def __str__(self):
        items_str = "\n   ".join([str(item) for item in self.items])
        return (f"{self.name} (total weight: {self.empty_weight + self.current_weight}, "
                f"empty weight: {self.empty_weight}, capacity: {self.current_weight}/{self.weight_capacity})\n   {items_str}")


class MultiContainer:
    def __init__(self, name):
        self.name = name
        self.compartments = []
        self.empty_weight = 0

    def add_compartment(self, compartment):
        #Adds compartment and updates the empty weight.#
        self.compartments.append(compartment)
        self.empty_weight += compartment.empty_weight

    def add_item(self, item):
        #Adds item to the first compartment with available capacity.#
        for compartment in self.compartments:
            if compartment.add_item(item):
                return True
        return False

    def __str__(self):
        total_weight = self.empty_weight + sum(compartment.current_weight for compartment in self.compartments)
        compartments_str = "\n   ".join([str(compartment) for compartment in self.compartments])
        return f"{self.name} (total weight: {total_weight}, empty weight: {self.empty_weight}, capacity: 0/0)\n   {compartments_str}"


def load_items(filename):
    #Loads items from CSV file.#
    items = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item_name = row['Name'].strip()
            item_weight = int(row[' Weight'].strip())
            items.append(Item(item_name, item_weight))
    return items


def load_compartments_data(filename):
    #Loads compartment details from CSV into a dictionary.#
    compartments = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name'].strip()
            empty_weight = int(row[' Empty Weight'].strip())
            weight_capacity = int(row[' Weight Capacity'].strip())
            compartments[name] = (empty_weight, weight_capacity)
    return compartments


def load_single_containers(filename):
    #Creates single-compartment containers from CSV data.#
    containers = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['Name'].strip()
            empty_weight = int(row[' Empty Weight'].strip())
            weight_capacity = int(row[' Weight Capacity'].strip())
            container = MultiContainer(name)
            container.add_compartment(Compartment(name, empty_weight, weight_capacity))
            containers.append(container)
    return containers


def load_multi_containers(filename, compartments_data):
    #Creates multi-compartment containers based on CSV data and compartment details.#
    containers = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            container_name = row[0].strip()
            compartment_names = [compartment.strip() for compartment in row[1:]]
            multi_container = MultiContainer(container_name)
            for name in compartment_names:
                empty_weight, weight_capacity = compartments_data.get(name, (1, 1000))
                multi_container.add_compartment(Compartment(name, empty_weight, weight_capacity))
            containers.append(multi_container)
    return containers


def initialize_game_data():
    #Initializes items and containers data from CSV files.#
    items = load_items('data/items.csv')
    compartments_data = load_compartments_data('data/containers.csv')
    single_containers = load_single_containers('data/containers.csv')
    multi_containers = load_multi_containers('data/multi_containers.csv', compartments_data)
    all_containers = single_containers + multi_containers
    print("="*50)
    print(f"Initialized {len(items)} items including {len(all_containers)} containers.")
    return items, all_containers


def select_container(all_containers):
    #Prompts user to select a container by name.#
    while True:
        container_name = input("Enter the name of the container: ").strip().lower()
        for container in all_containers:
            if container.name.lower() == container_name:
                return container
        print(f'"{container_name}" not found. Try again.')


def display_menu():
    #Displays the main menu and returns user's choice.#
    print("\n==================================")
    print("Enter your choice:")
    print("1. Loot item.")
    print("2. List looted items.")
    print("0. Quit.")
    print("==================================")
    return input("Your choice: ").strip()


def main():
    #Main game loop for the looting system.#
    items, all_containers = initialize_game_data()
    selected_container = select_container(all_containers)

    while True:
        choice = display_menu()
        
        if choice == "1":
            item_name = input("Enter the name of the item: ").strip().lower()
            item_to_loot = next((item for item in items if item.name.lower() == item_name), None)
            if not item_to_loot:
                print(f'"{item_name}" not found. Try again.')
            elif selected_container.add_item(item_to_loot):
                print(f'Success! Item "{item_name}" stored in container "{selected_container.name}".')
            else:
                print(f'Failure! Item "{item_name}" NOT stored in container "{selected_container.name}".')

        elif choice == "2":
            print(f"\n{selected_container}")

        elif choice == "0":
            print("Exiting the game.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
