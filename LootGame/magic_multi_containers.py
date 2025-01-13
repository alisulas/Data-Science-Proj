import csv

# Define the Item class
class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __str__(self):
        return f"{self.name} (weight: {self.weight})"

# Define the base Container class
class Container:
    def __init__(self, name, empty_weight=0, capacity=0):
        self.name = name
        self.empty_weight = empty_weight
        self.capacity = capacity
        self.current_weight = 0
        self.items = []
        self.sub_containers = []

    def can_add_item(self, item):
        return self.current_weight + item.weight <= self.capacity

    def add_item(self, item):
        if self.can_add_item(item):
            self.items.append(item)
            self.current_weight += item.weight
            return True
        return False

    def add_sub_container(self, container):
        self.sub_containers.append(container)
        self.empty_weight += container.empty_weight

    def __str__(self, level=0):
        indent = " " * level
        items_str = "\n".join([f"{indent}    {item}" for item in self.items]) if self.items else ""
        
        container_info = (f"{indent}{self.name} (total weight: {self.empty_weight + self.current_weight}, "
                          f"empty weight: {self.empty_weight}, capacity: {self.current_weight}/{self.capacity})")
        
        if items_str:
            container_info += f"\n{items_str}"

        # Append sub-containers
        for sub in self.sub_containers:
            container_info += f"\n{sub.__str__(level + 1)}"
            
        return container_info


class MagicMultiContainer(Container):
    def __init__(self, name, empty_weight=0):
        super().__init__(name, empty_weight, capacity=0)  

    def add_item(self, item):
        for sub_container in self.sub_containers:
            if sub_container.add_item(item):
                return True
        return False

    def __str__(self, level=0):
        return super().__str__(level)

# Define the MagicContainer class inheriting from Container
class MagicContainer(Container):
    def __init__(self, name, empty_weight=0):
        super().__init__(name, empty_weight, capacity=0) 

    def add_item(self, item):
        for sub_container in self.sub_containers:
            if sub_container.add_item(item):
                return True
        return False

    def __str__(self, level=0):
        return super().__str__(level)

# 
def load_compartments_data(filename):
    compartments = {}
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:   
                try:
                    name = row['Name'].strip()
                    empty_weight = int(row[' Empty Weight'].strip())
                    capacity = int(row[' Weight Capacity'].strip())
                    compartments[name] = (empty_weight, capacity)
                except ValueError as ve:
                    print(f"Error parsing compartment: {row}. Error: {ve}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return compartments

# 
# 
def load_single_containers(filename):
    containers = {}
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    name = row['Name'].strip()
                    empty_weight = int(row[' Empty Weight'].strip())
                    capacity = int(row[' Weight Capacity'].strip())
                    container = Container(name, empty_weight, capacity)
                    containers[name] = container
                except ValueError as ve:
                    print(f"Error parsing container: {row}. Error: {ve}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return containers

# multi_containers.csv, dict of empty weight and capacity, 
def load_multi_containers(filename, compartments_data, container_map):
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip header
            for row in reader:
                if not row:
                    continue  # Skip empty rows
                container_name = row[0].strip()
                magic_container = MagicMultiContainer(container_name) #MultiBox1, MultiBox2 - name of multicontainers.csv
                for compartment_name in row[1:]:     #content of MultiBox = Box1, Box2
                    compartment_name = compartment_name.strip()  #Box1, Box2
                    if compartment_name in container_map:
                        # If the compartment is already a container, add it as a sub-container
                        magic_container.add_sub_container(container_map[compartment_name]) #data of Box1
                    elif compartment_name in compartments_data:
                        # If the compartment is defined in containers.csv, create a Container
                        empty_weight, capacity = compartments_data[compartment_name]
                        compartment = Container(compartment_name, empty_weight, capacity)
                        container_map[compartment_name] = compartment
                        magic_container.add_sub_container(compartment)
                    else:
                        # Handle undefined compartments
                        print(f"Warning: Compartment '{compartment_name}' not found in compartments_data. Using default values.")
                        compartment = Container(compartment_name, 0, 0)
                        container_map[compartment_name] = compartment
                        magic_container.add_sub_container(compartment)
                container_map[container_name] = magic_container
    except FileNotFoundError:
        print(f"File {filename} not found.")

# 
def load_magic_multi_containers(filename, compartments_data, container_map):
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Skip header
            for row in reader:
                if not row:
                    continue  # Skip empty rows
                container_name = row[0].strip()
                magic_container = MagicMultiContainer(container_name)
                for compartment_name in row[1:]:
                    compartment_name = compartment_name.strip()
                    if compartment_name in container_map:
                        # If the compartment is already a container, add it as a sub-container
                        magic_container.add_sub_container(container_map[compartment_name])
                    elif compartment_name in compartments_data:
                        # If the compartment is defined in containers.csv, create a Container
                        empty_weight, capacity = compartments_data[compartment_name]
                        compartment = Container(compartment_name, empty_weight, capacity)
                        container_map[compartment_name] = compartment
                        magic_container.add_sub_container(compartment)
                    else:
                        # Handle undefined compartments
                        print(f"Warning: Compartment '{compartment_name}' not found in compartments_data. Using default values.")
                        compartment = Container(compartment_name, 0, 0)
                        container_map[compartment_name] = compartment
                        magic_container.add_sub_container(compartment)
                container_map[container_name] = magic_container
    except FileNotFoundError:
        print(f"File {filename} not found.")

# 
def load_magic_containers(filename, compartments_data, container_map):
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    container_name = row['Name'].strip()
                    sub_container_name = row[' Container'].strip()
                    magic_container = MagicContainer(container_name)
                    if sub_container_name in container_map:
                        # If the sub-container is already a container, add it as a sub-container
                        magic_container.add_sub_container(container_map[sub_container_name])
                    elif sub_container_name in compartments_data:
                        # If the sub-container is defined in containers.csv, create a Container
                        empty_weight, capacity = compartments_data[sub_container_name]
                        sub_container = Container(sub_container_name, empty_weight, capacity)
                        container_map[sub_container_name] = sub_container
                        magic_container.add_sub_container(sub_container)
                    else:
                        # Handle undefined sub-containers
                        print(f"Warning: Sub-container '{sub_container_name}' not found in compartments_data. Using default values.")
                        sub_container = Container(sub_container_name, 0, 0)
                        container_map[sub_container_name] = sub_container
                        magic_container.add_sub_container(sub_container)
                    container_map[container_name] = magic_container
                except ValueError as ve:
                    print(f"Error parsing magic container: {row}. Error: {ve}")
    except FileNotFoundError:
        print(f"File {filename} not found.")


# 
def load_items(filename):
    items = []
    try:
        with open(filename, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    item = Item(row['Name'].strip(), int(row[' Weight'].strip()))
                    items.append(item)
                except ValueError as ve:
                    print(f"Error parsing item: {row}. Error: {ve}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return items

# Select container
def select_container(all_containers):    #all container_map dict passed which is object of Container or Multicontainer
    container_names = [container.name for container in all_containers.values()] #["Box1", "Box2", "MultiBox1"]
    while True:
        container_name = input("Enter the name of the container: ").strip()
        for container in all_containers.values():
            if container.name.lower() == container_name.lower():
                return container
        print(f'"{container_name}" not found. Please choose from the available containers.')

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
            item_name = input("Enter the name of the item to loot: ").strip()
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
    compartments_data = load_compartments_data('data/containers.csv')   #dicts --> {'Box1': (1, 50)}
    container_map = {}
    
    # Load single-compartment containers
    single_containers = load_single_containers('data/containers.csv')   #Container Object -> Box1
    container_map.update(single_containers)
    

    load_multi_containers('data/multi_containers.csv', compartments_data, container_map)  #MagicMultiContainer Object "MultiBox1" with sub [Box1, Box2]. container_map['MultiBox1']
    
   
    load_magic_multi_containers('data/magic_multi_containers.csv', compartments_data, container_map) #MagicMultiContainer Object MagicMulti1 with MultiBox1. container_map['MagicMulti1']
    
  
    load_magic_containers('data/magic_containers.csv', compartments_data, container_map)
    
    # Load items
    items = load_items('data/items.csv')  #list of Item Object
    

    print(f"\nInitialized {len(items)} items including {len(container_map)} containers.")
    
    if not container_map:
        print("No containers available. Exiting.")˘
        return
    
    selected_container = select_container(container_map)
    main_menu(selected_container, items)

if __name__ == "__main__":
    main()
