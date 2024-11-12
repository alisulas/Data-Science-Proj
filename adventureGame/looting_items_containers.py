from items_and_containers import *


#function to display main menu
def display_menu():
    print("==================================")
    print("Enter your choice:")
    print("1. Loot item.")
    print("2. List looted items.")
    print("0. Quit.")
    print("==================================")

#define a class to loot and list items int the container
class LootItemContainer(Container):
    def __init__(self, name, empty_weight, capacity):
        super().__init__(name, empty_weight, capacity)
        self.loot = []
        self.count = 0
        self.top = -1
        self.total_weight = empty_weight

    #function to loot items to the container
    def loot_item(self):
        while True:
            item_name = input("Enter the name of the item: ")
            items_looted = None
            for item in items:
                if item.name == item_name:
                    items_looted = item
                    break
            if items_looted:
                self.loot.append((items_looted.name, items_looted.weight)) 
                print("Success! Item " + "'" + items_looted.name + "'" +  " stored in container " + "'" + self.name + "'")
                self.top += 1
                self.count += 1
                self.total_weight += items_looted.weight
                break
            else:
                print("'" + item_name  + "'" + " not found. Try again") 
                print("Failure! Item " + "'" + item_name + "'" + " NOT stored in container " + "'" + self.name + "'")
    
    #function to list items in the container           
    def list_looted_items(self):
        print(f"{self.name} (total weight: {self.total_weight}, empty weight: {self.empty_weight}, capacity: {self.total_weight - self.empty_weight}/{self.capacity})")
        for item in self.loot:
            print(f"   {item[0]} (weight: {item[1]})")

# Main program to load data and display output
items = load_items('data/items.csv') 
containers = load_containers('data/containers.csv')
            
# function to list items
item_list = []
for item in items:
    item_list.append(item.name)

# function for user to input and choose a container
container_list = []
for container in containers:
    container_list.append(container.name)
            
while True:
    container_input = input("Enter the name of the container: ")
    if container_input in container_list:
        break
    else:
        print("'" + container_input + "'" + " not found. Try again.")
              
# Find the selected container's details
selected_container = None
for container in containers:
    if container.name == container_input:
        selected_container = container
        break
if selected_container:
    container_used = LootItemContainer(selected_container.name, selected_container.empty_weight, selected_container.capacity)
else:
    print("Error: Selected container not found.")
    container_used = None

# function for users to choose menu
while container_used:
    display_menu()
    choice = input("Enter your choice: ")
    if choice == "1":
        container_used.loot_item()
    elif choice == "2":
        container_used.list_looted_items()
    elif choice == "0":
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please try again.")


# In[ ]:

