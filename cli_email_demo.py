from __future__ import annotations

from typing import List

from email_server.email_server import Email_server
from email_server.email_models import Email_message


def create_demo_server() -> Email_server:
    server = Email_server(capacity=32)
    server.add_user(1, "Alice", "alice@example.com")
    server.add_user(2, "Bob", "bob@example.com")
    server.add_user(3, "Charlie", "charlie@example.com")
    server.add_user(4, "Diana", "diana@example.com")
    return server


def print_menu() -> None:
    print("\n=== EMAIL SERVER DEMO ===")
    print("1. List users")
    print("2. Send email")
    print("3. View inbox")
    print("4. View sent items")
    print("5. Process outbound queue now")
    print("0. Quit")


def list_users(server: Email_server) -> None:
    print("\nRegistered users:")
    for bucket in server.users.buckets:
        for _, user in bucket:
            print(f"{user.user_id}: {user.name} <{user.email_address}>")


def read_body_from_input() -> str:
    print("Body (finish with a single '.' on its own line):")
    lines: List[str] = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    return "\n".join(lines)


def send_email_via_cli(server: Email_server) -> None:
    try:
        sender_id = int(input("Sender user ID: ").strip())
        receiver_id = int(input("Receiver user ID: ").strip())
    except ValueError:
        print("User IDs must be integers.")
        return

    subject = input("Subject: ").strip()
    body = read_body_from_input()

    try:
        server.send_email(sender_id, receiver_id, subject, body)
        print("Email queued for delivery.")
    except KeyError as exc:
        print(f"Error sending email: {exc}")


def view_inbox(server: Email_server) -> None:
    try:
        user_id = int(input("User ID to view inbox: ").strip())
    except ValueError:
        print("User ID must be an integer.")
        return

    sort_choice = input("Sort by (t)ime or (s)ender [t/s]: ").strip().lower()
    sort_by = "time" if sort_choice != "s" else "sender"

    try:
        inbox = server.get_inbox(user_id, sort_by=sort_by)
    except KeyError:
        print("No such user.")
        return

    if not inbox:
        print("Inbox is empty.")
        return

    print(f"\nInbox for user {user_id}:")
    for index, msg in enumerate(inbox, start=1):
        print("--------------------------------------------------")
        print(f"{index}. From: {msg.sender_id}")
        print(f"   To:   {msg.receiver_id}")
        print(f"   Subject: {msg.subject}")
        print(f"   Time: {msg.timestamp}")
        print("   Body:")
        print(msg.body)


def view_sent_items(server: Email_server) -> None:
    try:
        user_id = int(input("User ID to view sent items: ").strip())
    except ValueError:
        print("User ID must be an integer.")
        return

    mailbox = server.mailboxes.get(user_id)
    if mailbox is None or not mailbox.sent_items:
        print("No sent items for this user.")
        return

    print(f"\nSent items for user {user_id}:")
    for index, msg in enumerate(mailbox.sent_items, start=1):
        print("--------------------------------------------------")
        print(f"{index}. From: {msg.sender_id}")
        print(f"   To:   {msg.receiver_id}")
        print(f"   Subject: {msg.subject}")
        print(f"   Time: {msg.timestamp}")
        print("   Body:")
        print(msg.body)


def process_outbound_queue(server: Email_server) -> None:
    server.process_outbound_queue()
    print("Outbound queue processed.")


def main() -> None:
    server = create_demo_server()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_users(server)
        elif choice == "2":
            send_email_via_cli(server)
        elif choice == "3":
            view_inbox(server)
        elif choice == "4":
            view_sent_items(server)
        elif choice == "5":
            process_outbound_queue(server)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Unknown option, please try again.")


if __name__ == "__main__":
    main()
