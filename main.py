"""
Digital Notes Management System
PS No. 65 | Python 3

Stores notes permanently in notes.txt using the format:
ID|Title|Content

Run:
    python main.py
"""

from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "notes.txt"


def load_notes():
    """Load notes from the text file. Content may contain additional | characters."""
    notes = []
    if not DATA_FILE.exists():
        DATA_FILE.touch()
        return notes

    with DATA_FILE.open("r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n\r")
            if not line.strip():
                continue
            parts = line.split("|", 2)
            if len(parts) != 3:
                # Ignore malformed lines rather than crashing the whole program.
                continue
            note_id, title, content = parts
            notes.append({"id": note_id, "title": title, "content": content})
    return notes


def save_notes(notes):
    """Save all notes to disk in ID|Title|Content format."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        for note in notes:
            # Keep each note on one physical line.
            title = note["title"].replace("\n", " ").replace("\r", " ")
            content = note["content"].replace("\n", " ").replace("\r", " ")
            file.write(f'{note["id"]}|{title}|{content}\n')


def next_note_id(notes):
    """Return the next N-number ID without reusing IDs after deletion."""
    largest = 0
    for note in notes:
        note_id = note["id"]
        if note_id.startswith("N") and note_id[1:].isdigit():
            largest = max(largest, int(note_id[1:]))
    return f"N{largest + 1}"


def add_note(notes):
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty. Note not saved.")
        return

    content = input("Content: ").strip()
    note_id = next_note_id(notes)
    notes.append({"id": note_id, "title": title, "content": content})
    save_notes(notes)
    print(f"Note saved. ID: {note_id} | {title}")


def view_notes(notes):
    if not notes:
        print("No notes found.")
        return

    for note in notes:
        print(f'{note["id"]} | {note["title"]} | {note["content"]}')


def search_notes(notes):
    keyword = input("Keyword: ").strip().casefold()
    if not keyword:
        print("Search keyword cannot be empty.")
        return

    matches = [
        note for note in notes
        if keyword in note["title"].casefold()
        or keyword in note["content"].casefold()
    ]
    if not matches:
        print("No matching notes found.")
        return

    for note in matches:
        print(f'{note["id"]} | {note["title"]} | {note["content"]}')


def edit_note(notes):
    note_id = input("Enter note ID to edit: ").strip().upper()
    note = next((item for item in notes if item["id"].upper() == note_id), None)
    if note is None:
        print(f"Note ID {note_id} does not exist.")
        return

    new_content = input("New content: ").strip()
    note["content"] = new_content
    save_notes(notes)
    print(f"Note {note_id} updated.")


def delete_note(notes):
    note_id = input("Enter note ID to delete: ").strip().upper()
    note = next((item for item in notes if item["id"].upper() == note_id), None)
    if note is None:
        print(f"Note ID {note_id} does not exist.")
        return

    notes.remove(note)
    save_notes(notes)
    print(f"Note {note_id} deleted. Notes left: {len(notes)}")


def display_menu():
    print("\n========== DIGITAL NOTES MANAGEMENT SYSTEM ==========")
    print("1. Add note")
    print("2. View all notes")
    print("3. Search notes")
    print("4. Edit note")
    print("5. Delete note")
    print("6. Reload notes from file")
    print("0. Exit")
    print("======================================================")


def main():
    notes = load_notes()
    print("Welcome to Digital Notes Management System!")
    print(f"Loaded {len(notes)} note(s).")

    while True:
        display_menu()
        choice = input("Enter menu option: ").strip()

        if choice == "1":
            add_note(notes)
        elif choice == "2":
            view_notes(notes)
        elif choice == "3":
            search_notes(notes)
        elif choice == "4":
            edit_note(notes)
        elif choice == "5":
            delete_note(notes)
        elif choice == "6":
            notes = load_notes()
            print(f"Reloaded {len(notes)} note(s).")
        elif choice == "0":
            print("Thank you for using Digital Notes Management System.")
            break
        else:
            print("Invalid menu option. Please choose 0 to 6.")


if __name__ == "__main__":
    main()
