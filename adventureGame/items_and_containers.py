import csv

# Define the Item class
class Item:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
    
    def __str__(self):
        return f"{self.name} (weight: {self.weight})"

# Define the Container class, which inherits from Item
class Container(Item):
    def __init__(self, name, empty_weight, capacity):
        super().__init__(name, empty_weight)  # Initialize as an Item
        self.empty_weight = empty_weight
        self.capacity = capacity

    def __str__(self):
        return (f"{self.name} (total weight: {self.empty_weight}, "
                f"empty weight: {self.empty_weight}, capacity: 0/{self.capacity})")

# Function to load items from items.csv
def load_items(filename):
    items = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            item = Item(row['Name'].strip(), int(row[' Weight'].strip()))
            items.append(item)
    return items

# Function to load containers from containers.csv
def load_containers(filename):
    containers = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            container = Container(row['Name'].strip(), 
                                  int(row[' Empty Weight'].strip()), 
                                  int(row[' Weight Capacity'].strip()))
            containers.append(container)
    return containers

# Main program to load data and display output
items = load_items('data/items.csv')              # Path adjusted to data folder
containers = load_containers('data/containers.csv')  # Path adjusted to data folder

# Sort items and containers separately by name
sorted_items = sorted(items, key=lambda x: x.name)
sorted_containers = sorted(containers, key=lambda x: x.name)

# Display output
print(f"Initialized {len(items) + len(containers)} items including {len(containers)} containers.")

print("\nItems:")
for item in sorted_items:
    print(item)

print("\nContainers:")
for container in sorted_containers:
    print(container)





