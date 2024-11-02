#Ask user to roll the dice
#if enters Y, then generate two random integer and print them
#if enters N, print thank you and terminate
#else print error message invalid input


import random


while True:
    user_input = str(input("Want to roll the dice? (y/n): "))
    if user_input.lower() == 'y':
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        print(f"You rolled {die1} and {die2}")
    elif user_input.lower() == 'n':
        print("thank you")
        break
    else:
        print("input is not valid")


