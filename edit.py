import sys
import os
import json
import time


def main_menu():
    print("============================== Ardventure Editor ===============================")
    print("Edit and create Ardventure maps.")
    print()
    print("Select an option:")
    print("[c] Create a new map")
    print("[l] Load an existing map")
    print("[q] Quit")

    choice = input("Choice: ")

    if choice == "c":
        create_map()
    elif choice == "l":
        print("Enter path to map file:")
        path = input("Path: ")
        # Read in the map file into map_data
        with open(path, 'r') as f:
            map_data = json.load(f)
        current_room = map_data["starting_room"]
        edit_map(map_data)
        # TODO: Add error handling for path.
        # TODO: Add option to view/load recent map files.
    elif choice == "q":
        print("Quitting.")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")
        main_menu()


def create_map():
    print("================================== Create Map ==================================")
    print("Specify metadata:")
    print("Enter a friendly name for the map, such as 'The Starting Zone'")
    name = input("Name: ")
    print("Brief Description, such as 'This is the starting area of the game'")
    description = input("Description: ")
    print("Enter the starting room ID (The room you start in) and the room ID range.")
    starting_room = input("Starting Room ID: ")
    room_id_start = int(input("Starting ID: "))
    room_id_end = int(input("Ending ID: "))
    print("Enter path to save map:")
    path = input("Path: ")

    map_data = {
        "name": name,
        "description": description,
        "path": path,
        "starting_room": starting_room,
        "room_id_start": room_id_start,
        "room_id_end": room_id_end,
        "rooms": {}
    }

    for i in range(room_id_start, room_id_end + 1):
        map_data["rooms"][str(i)] = {
            "title": "Room " + str(i),
            "description": "Empty Room # " + str(i),
            "actions": {},
            "neighbors": {
                "n": -1,
                "e": -1,
                "w": -1,
                "s": -1
            }
        }

    print("Map created. Puting you at the starting room to start editing.")
    edit_map(map_data)


def edit_map(map_data):
    current_room = str(map_data["starting_room"])
    print("=================================== Map Editor =================================")
    print("Map Name: " + map_data["name"])
    print("Map Description: " + map_data["description"])
    print("Path: " + map_data["path"])
    print()

    print(map_data["rooms"][current_room]["title"])
    print("--------------------------------------------------------------------------------")
    print(map_data["rooms"][current_room]["description"])
    print("--------------------------------------------------------------------------------")
    # Print out each of the available actions
    print("Actions:")
    if (len(map_data["rooms"][current_room]["actions"]) == 0):
        print("No actions available.")
    else:
        for action in map_data["rooms"][current_room]["actions"]:
            print("[" + action + "] " + map_data["rooms"]
                  [current_room]["actions"][action])
    print()
    # Print each of the neighbors/directions if they are not -1
    print("Neighbors:")
    for direction in map_data["rooms"][current_room]["neighbors"]:
        if map_data["rooms"][current_room]["neighbors"][direction] != -1:
            print("[" + direction + "] [ID: " + str(map_data["rooms"][current_room]["neighbors"][direction]) + "]" + map_data["rooms"]
                  [str(map_data["rooms"][current_room]["neighbors"][direction])]["title"])
    print()
    print("[t] Edit title")
    print("[d] Edit description")
    print("[a] Add action")
    print("[r] Remove action")
    print("[n] Edit neighbor")
    print("[g] Go to room")
    print("[s] Save Map")
    print("[q] Quit")

    choice = input("> ")

    if choice == "t":
        print("Enter new title:")
        title = input("Title: ")
        map_data["rooms"][current_room]["title"] = title
        edit_map(map_data)
    elif choice == "d":
        print("Enter new description:")
        description = input("Description: ")
        map_data["rooms"][current_room]["description"] = description
        edit_map(map_data)
    elif choice == "a":
        print("Enter action key:")
        key = input("Key: ")
        print("Enter action description:")
        description = input("Description: ")
        map_data["rooms"][current_room]["actions"][key] = description
        edit_map(map_data)
    elif choice == "r":
        print("Enter action key to remove:")
        key = input("Key: ")
        del map_data["rooms"][current_room]["actions"][key]
        edit_map(map_data)
    elif choice == "n":
        print("Enter direction to edit:")
        direction = input("Direction: ")
        print("Enter room ID to connect to:")
        room_id = int(input("Room ID: "))
        map_data["rooms"][current_room]["neighbors"][direction] = room_id
        edit_map(map_data)
    elif choice == "g":  # TODO: Validate the room ID is in the map.
        print("Enter room ID to go to:")
        room_id = input("Room ID: ")
        current_room = room_id
        edit_map(map_data)
    elif choice == "s":
        with open(map_data["path"], 'w') as f:
            json.dump(map_data, f)
        print("Map saved")
        time.sleep(2)
        edit_map(map_data)
    elif choice == "q":
        print("Returning to Main Menu")
        main_menu()
    else:
        print("Invalid choice. Please try again.")
        edit_map(map_data)


if __name__ == "__main__":
    main_menu()
