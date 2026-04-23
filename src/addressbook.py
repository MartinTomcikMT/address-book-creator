from colorama import Fore, Style, init
import json
import csv
import os
from pathlib import Path

# Initialize colorama so colors reset automatically after each print
init(autoreset=True)

# Base directory for storing data files (goes two levels up from this file)
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
JSON_FILE = DATA_DIR / "contacts.json"
CSV_FILE = DATA_DIR / "contacts.csv"

# Simple ASCII banner shown at the top of the app
ASCII_ART = r"""
     ___       _______   _______  .______       _______     _______.  _______.   .______     ______     ______    __  ___ 
    /   \     |       \ |       \ |   _  \     |   ____|   /       | /       |   |   _  \   /  __  \   /  __  \  |  |/  / 
   /  ^  \    |  .--.  ||  .--.  ||  |_)  |    |  |__     |   (----`|   (----`   |  |_)  | |  |  |  | |  |  |  | |  '  /  
  /  /_\  \   |  |  |  ||  |  |  ||      /     |   __|     \   \     \   \       |   _  <  |  |  |  | |  |  |  | |    <   
 /  _____  \  |  '--'  ||  '--'  ||  |\  \----.|  |____.----)   |.----)   |      |  |_)  | |  `--'  | |  `--'  | |  .  \  
/__/     \__\ |_______/ |_______/ | _| `._____||_______|_______/ |_______/       |______/   \______/   \______/  |__|\__\ 
"""

# Print banner in red
def print_ascii_art():
    print(Fore.RED + ASCII_ART + Style.RESET_ALL)

# Clear terminal screen (works on Windows and Unix)
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# Clear screen and show banner
def show_header():
    clear_screen()
    print_ascii_art()

# Small pause so user can read output before returning to menu
def pause():
    input("\nPress Enter to return to menu...")

# Let user choose storage format (JSON or CSV)
def choose_file_type():
    while True:
        show_header()
        print("=== SELECT STORAGE FORMAT ===")
        print("1. JSON")
        print("2. CSV")

        choice = input("\nChoose format: ").strip()

        if choice == "1":
            return "json"
        elif choice == "2":
            return "csv"
        else:
            print("\nInvalid option.")
            pause()

# Load contacts from selected file type
def load_contacts(file_type):
    if file_type == "json":
        # If file doesn't exist, just return empty list
        if not JSON_FILE.exists():
            return []

        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # If file is broken, don't crash — just return empty list
            return []

    elif file_type == "csv":
        if not CSV_FILE.exists():
            return []

        contacts = []
        with open(CSV_FILE, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert each row into our contact structure
                contacts.append({
                    "name": row.get("name", ""),
                    "surname": row.get("surname", ""),
                    "address_name": row.get("address_name", ""),
                    "address_number": row.get("address_number", ""),
                    "city": row.get("city", ""),
                    "country": row.get("country", ""),
                    "phone": row.get("phone", ""),
                    "email": row.get("email", "")
                })
        return contacts

    return []

# Save contacts back to file
def save_contacts(contacts, file_type):
    # Make sure data folder exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if file_type == "json":
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(contacts, file, indent=4, ensure_ascii=False)

    elif file_type == "csv":
        with open(CSV_FILE, "w", encoding="utf-8", newline="") as file:
            fieldnames = [
                "name", "surname", "address_name", "address_number",
                "city", "country", "phone", "email"
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)

# Display contacts in two-column layout (left = personal, right = address)
def display_contacts(contacts):
    if not contacts:
        print("\nNo contacts found.")
        return
   
    for index, contact in enumerate(contacts, start=1):
        print(f"\nContact #{index}")

        # Left side = basic info
        left_column = [
            f"Name    : {contact.get('name', '-')}",
            f"Surname : {contact.get('surname', '-')}",
            f"Phone   : {contact.get('phone', '-')}",
            f"Email   : {contact.get('email', '-')}",
        ]

        # Right side = address info
        right_column = [
            f"Street  : {contact.get('address_name', '-')}",
            f"No.     : {contact.get('address_number', '-')}",
            f"City    : {contact.get('city', '-')}",
            f"Country : {contact.get('country', '-')}",
        ]

        col_width = 40  # spacing between columns

        for left, right in zip(left_column, right_column):
            print(f"{left.ljust(col_width)} | {right}")

        print("-" * 75)

# Helper for editing: keeps old value if user presses Enter
def update_field(current_value, label):
    new_value = input(f"{label} [{current_value}]: ").strip()
    return current_value if new_value == "" else new_value

# Edit selected contact
def edit_contact(contacts, file_type):
    if not contacts:
        print("\nNo contacts to edit.")
        return

    display_contacts(contacts)

    try:
        edit_choice = int(input("\nEnter contact number to edit: "))
        index = edit_choice - 1

        if index < 0 or index >= len(contacts):
            print("\nInvalid contact number.")
            return

        contact = contacts[index]

        show_header()
        print(f"=== EDIT CONTACT #{edit_choice} ===")
        print("Press Enter to keep the current value.\n")

        # Update each field one by one
        contact["name"] = update_field(contact.get("name", ""), "Name")
        contact["surname"] = update_field(contact.get("surname", ""), "Surname")
        contact["address_name"] = update_field(contact.get("address_name", ""), "Street name")
        contact["address_number"] = update_field(contact.get("address_number", ""), "Street number")
        contact["city"] = update_field(contact.get("city", ""), "City")
        contact["country"] = update_field(contact.get("country", ""), "Country")
        contact["phone"] = update_field(contact.get("phone", ""), "Phone")
        contact["email"] = update_field(contact.get("email", ""), "Email")

        save_contacts(contacts, file_type)
        print("\nContact updated successfully.")

    except ValueError:
        print("\nPlease enter a valid number.")

# Main loop of the program
def main():
    file_type = choose_file_type()
    contacts = load_contacts(file_type)

    while True:
        show_header()
        print(f"Current format : {file_type.upper()}")
        print(f"Loaded contacts: {len(contacts)}")
        print("\n=== Address Book Creator ===")
        print("1. Add contact")
        print("2. View contacts")
        print("3. Edit contact")
        print("4. Delete contact")
        print("5. Change file format")
        print("6. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            show_header()
            print("=== ADD CONTACT ===")

            # Collect user input
            name = input("Enter name: ").strip()
            surname = input("Enter surname: ").strip()
            address_name = input("Enter street name: ").strip()
            address_number = input("Enter street number: ").strip()
            city = input("Enter city: ").strip()
            country = input("Enter country: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email: ").strip()

            # Create new contact
            contact = {
                "name": name,
                "surname": surname,
                "address_name": address_name,
                "address_number": address_number,
                "city": city,
                "country": country,
                "phone": phone,
                "email": email
            }

            contacts.append(contact)
            save_contacts(contacts, file_type)

            print("\nContact added successfully.")
            pause()

        elif choice == "2":
            show_header()
            print("=== VIEW CONTACTS ===")
            display_contacts(contacts)
            pause()

        elif choice == "3":
            show_header()
            print("=== EDIT CONTACT ===")
            edit_contact(contacts, file_type)
            pause()

        elif choice == "4":
            show_header()
            print("=== DELETE CONTACT ===")

            if not contacts:
                print("\nNo contacts to delete.")
                pause()
                continue

            display_contacts(contacts)

            try:
                delete_choice = int(input("\nEnter contact number to delete: "))
                index = delete_choice - 1

                if index < 0 or index >= len(contacts):
                    print("\nInvalid contact number.")
                else:
                    removed = contacts.pop(index)
                    save_contacts(contacts, file_type)
                    print(f"\nDeleted contact: {removed['name']} {removed['surname']}")
            except ValueError:
                print("\nPlease enter a valid number.")

            pause()

        elif choice == "5":
            file_type = choose_file_type()
            contacts = load_contacts(file_type)

        elif choice == "6":
            save_contacts(contacts, file_type)
            show_header()
            print("Goodbye.")
            break

        else:
            show_header()
            print("Invalid option.")
            pause()

if __name__ == "__main__":
    main()