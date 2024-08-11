import sys
import json
import time


def main_menu():
    print_centered("Ardventure Editor")
    print("Edit and create Ardventure maps.")
    print()
    print("Select an option:")
    print("[c] Create a new map")
    print("[l] Load an existing map")
    print("[v] Convert a map file to code to be used in Ardventure code.")
    print("[q] Quit")

    choice = input("Choice: ")

    if choice == "c":
        create_map()
    elif choice == "l":
        print("Enter path to map file:")
        path = input("Path: ")
        # Check if path ends in .map, if not, add it
        if not path.endswith(".map"):
            path += ".map"
        # Read in the map file into map_data
        try:
            with open(path, 'r', encoding='utf-8') as f:
                map_data = json.load(f)
            edit_map(map_data)
        except FileNotFoundError:
            print("File not found. Please try again.")
            main_menu()
        except json.decoder.JSONDecodeError:
            print("Invalid JSON file format. Please try a different file.")
            main_menu()
    elif choice == "v":
        print("Enter path to map file:")
        path = input("Path: ")
        # Check if path ends in .map, if not, add it
        if not path.endswith(".map"):
            path += ".map"
        print("Enter path to save map code:")
        output_path = input("Path: ")
        if not output_path.endswith(".txt"):
            output_path += ".txt"
        # Read in the map file into map_data
        try:
            with open(path, 'r', encoding='utf-8') as f:
                map_data = json.load(f)
            print("Converting map to code...")

            convert_map(map_data, output_path)

            main_menu()
        except FileNotFoundError:
            print("File not found. Please try again.")
            main_menu()
        except json.decoder.JSONDecodeError:
            print("Invalid JSON file format. Please try a different file.")
            main_menu()
    elif choice == "q":
        print("Quitting.")
        sys.exit()
    else:
        print("Invalid choice. Please try again.")
        main_menu()


def create_map():
    print_centered("Create Map")
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
    # Check if path ends in .map, if not, add it
    if not path.endswith(".map"):
        path += ".map"

    map_data = {
        "name": name,
        "description": description,
        "path": path,
        "starting_room": starting_room,
        "current_room": starting_room,
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
    current_room = map_data["current_room"]
    if current_room not in map_data["rooms"]:
        current_room = str(map_data["starting_room"])
    print_centered("Map Editor")
    print("Map Name: " + map_data["name"])
    print("Map Description: " + map_data["description"])
    print("Path: " + map_data["path"])
    print()

    print(map_data["rooms"][current_room]["title"])
    print("-" * 80)
    print(map_data["rooms"][current_room]["description"])
    print("-" * 80)
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
    print("[n] Edit/Add neighbor")
    print("[e] Delete neighbor")
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
        # Add the reverse direction to the neighbor room
        if direction == "n":
            reverse_direction = "s"
        elif direction == "s":
            reverse_direction = "n"
        elif direction == "e":
            reverse_direction = "w"
        elif direction == "w":
            reverse_direction = "e"
        map_data["rooms"][str(room_id)]["neighbors"][reverse_direction] = int(
            current_room)
        edit_map(map_data)
    elif choice == "e":
        print("Enter direction to delete:")
        direction = input("Direction: ")
        map_data["rooms"][current_room]["neighbors"][direction] = -1
        edit_map(map_data)
    elif choice == "g":  # TODO: Validate the room ID is in the map.
        print("Enter room ID to go to:")
        room_id = input("Room ID: ")
        map_data["current_room"] = room_id
        edit_map(map_data)
    elif choice == "s":
        with open(map_data["path"], 'w', encoding='utf-8') as f:
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


def convert_map(map_data, path):
    output = ""
    for room_id, room_data in map_data["rooms"].items():
        output += "{" + str(room_id) + ", \"" + \
            room_data["title"] + "\", \"" + room_data["description"] + "\", "
        if len(room_data["actions"]) > 0:
            actions = ""
            action_keys = ""
            for action_key, action_description in room_data["actions"].items():
                actions += "[" + action_key + "] " + action_description + "\\n"
                action_keys += "\"" + action_key + "\", "
            output += "\"" + actions.strip() + "\", "
        else:
            output += "\"\", "
            action_keys = ""
        directions = ""
        for direction, neighbor_id in room_data["neighbors"].items():
            if neighbor_id != -1:
                directions += "\"" + direction + "\", "
        output += "{" + action_keys + directions.strip(", ") + "}, "
        neighbors = ""
        for neighbor_id in room_data["neighbors"].values():
            neighbors += str(neighbor_id) + ", "
        output += "{" + neighbors.strip(", ") + "}},\n"

    with open(path, "w", encoding='utf-8') as f:
        # Strip the last comma and newline character
        f.write(output.rstrip(",\n"))
    print("Map code written to " + path)
    time.sleep(2)


def print_centered(text, pad="=", line_length=80):
    padding_length = (line_length - len(text)) // 2
    padding = pad * padding_length
    centered_text = f"{padding} {text} {padding}"
    if len(centered_text) < line_length:
        centered_text += pad
    print(centered_text)


if __name__ == "__main__":
    main_menu()
