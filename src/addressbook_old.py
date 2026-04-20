import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "contacts.json"


def load_contacts():
    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_contacts(contacts):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=2, ensure_ascii=False)

def main():
    contacts = load_contacts()
    print("Loaded contacts:", contacts)

    while True:
        print("\n=== Address Book Creator ===")
        print("1. Add contact")
        print("2. View contacts")
        print("3. Delete contact")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Enter name: ").strip()
            phone = input("Enter phone: ").strip()
            email = input("Enter email: ").strip()

            contact = {
                "name": name,
                "phone": phone,
                "email": email
            }

            contacts.append(contact)
            save_contacts(contacts)
         
            print("Contact added successfully.")
        elif choice == "2":
            if not contacts:
                print("No contacts found.")
            else:
                print("\nContacts:")
                for index, contact in enumerate(contacts, start=1):
                    print(f"{index}. Name: {contact['name']}, Phone: {contact['phone']}, Email: {contact['email']}")
        elif choice == "3":
            if not contacts:
                print("No contacts to delete.")
                continue
            print("\nContacts:")
            for index, contact in enumerate(contacts, start=1):
                print(f"{index}. {contact['name']}")

            try:
                choice = int(input("Enter contact number to delete: "))
                index = choice - 1

                if index < 0 or index >= len(contacts):
                    print("Invalid contact number.")
                else:
                    removed = contacts.pop(index)
                    save_contacts(contacts)
                    print(f"Deleted contact: {removed['name']}")
            except ValueError: 
                print("Please enter a valid number.")
        elif choice == "4":
            save_contacts(contacts)
            print("Goodbye.")                
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
