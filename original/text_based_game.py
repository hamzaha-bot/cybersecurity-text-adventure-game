
# Hamzah A.

def show_instructions():
    """Display the game objective and available commands."""
    print("Cybersecurity Attack Text Adventure Game")
    print("Collect all 6 security tools before entering the Control Room.")
    print("Move commands: go north, go south, go east, go west")
    print("Get item command: get <item name>")


def show_status(current_room, inventory, rooms):
    """Display the player's current game status."""
    print(f"\nYou are in the {current_room}")
    print(f"Inventory: {inventory}")

    if "item" in rooms[current_room]:
        print(f"You see a {rooms[current_room]['item']}")

    print("---------------------------")



def main():
    """Run the main gameplay loop."""
    # Dictionary linking rooms, directions, and items.
    rooms = {
        "Main Lobby": {
            "west": "Security Office",
            "north": "Control Room"
        },
        "Security Office": {
            "east": "Main Lobby",
            "north": "Network Operations Center",
            "item": "MFA Token"
        },
        "Network Operations Center": {
            "south": "Security Office",
            "north": "IT Office",
            "item": "Firewall Key"
        },
        "IT Office": {
            "south": "Network Operations Center",
            "east": "Server Room",
            "item": "Security Patch"
        },
        "Server Room": {
            "west": "IT Office",
            "east": "Data Center",
            "item": "Backup Drive"
        },
        "Data Center": {
            "west": "Server Room",
            "south": "Admin Office",
            "item": "Encryption Key"
        },
        "Admin Office": {
            "north": "Data Center",
            "west": "Control Room",
            "item": "Access Card"
        },
        "Control Room": {
            "south": "Main Lobby",
            "east": "Admin Office",
            "item": "Ransomware Bot"
        }
    }

    # Set the player's starting room.
    current_room = "Main Lobby"

    # Create an empty inventory for collected security tools.
    inventory = [] 

    # Show the game instructions before gameplay begins.
    show_instructions()

    # Continue the game until the player wins or loses.
    game_over = False

    while not game_over:
        show_status(current_room, inventory, rooms)

        # Check whether the player has entered the Control Room.
        if current_room == "Control Room":
            if len(inventory) == 6:
                print("Congratulations! You collected all 6 security tools and stopped the Ransomware Bot!")
            else:
                print("The Ransomware Bot has taken over the system. GAME OVER!")

            print("Thanks for playing the game. Hope you enjoyed it.")
            game_over = True
            continue

        command = input("Enter your move: ").lower().strip()

        # Handle movement commands.
        if command in ["go north", "go south", "go east", "go west"]:
            direction = command[3:]

            if direction in rooms[current_room]:
                current_room = rooms[current_room][direction]
            else:
                print("You can't go that way!")

        # Handle get-item commands.
        elif command.startswith("get "):
            requested_item = command[4:].strip()
            room_item = rooms[current_room].get("item")

            if room_item and requested_item == room_item.lower():
                inventory.append(room_item)
                del rooms[current_room]["item"]
                print(f"{room_item} retrieved!")
            else:
                print(f"Can't get {requested_item}!")
        else:
            print("Invalid command. Please try again.")



if __name__ == "__main__":
    main()
