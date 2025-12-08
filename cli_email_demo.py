from email_server.email_server import Email_server


def create_demo_server() -> Email_server:
    """Create an Email_server instance and pre-populate some demo users."""
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
    found_any = False
    for bucket in server.users.buckets:
        for user_id, user in bucket:
            found_any = True
            print(f"- ID: {user_id} | Name: {user.name} | Email: {user.email_address}")
    if not found_any:
        print("No users found.")


def send_email_via_cli(server: Email_server) -> None:
    try:
        sender_id = int(input("Sender user ID: ").strip())
        receiver_id = int(input("Receiver user ID: ").strip())
    except ValueError:
        print("User IDs must be integers.")
        return

    subject = input("Subject: ").strip()
    body_lines = []
    print("Body (enter a single '.' on its own line to finish):")
    while True:
        line = input()
        if line.strip() == ".":
            break
        body_lines.append(line)
    body = "\n".join(body_lines)

    server.send_email(
        sender_id=sender_id,
        receiver_id=receiver_id,
        subject=subject,
        body=body,
    )
    print("Email queued for delivery (still in outbound queue).")


def view_inbox(server: Email_server) -> None:
    try:
        user_id = int(input("User ID to view inbox: ").strip())
    except ValueError:
        print("User ID must be an integer.")
        return

    sort_choice = input("Sort by (t)ime or (s)ender? [t/s]: ").strip().lower()
    sort_by = "sender" if sort_choice == "s" else "time"

    inbox = server.get_inbox(user_id, sort_by=sort_by)
    if not inbox:
        print("Inbox is empty.")
        return

    print(f"\nInbox for user {user_id} (sorted by {sort_by}):")
    for i, msg in enumerate(inbox, start=1):
        print("--------------------------------------------------")
        print(f"Message #{i}")
        print(f"From: {msg.sender_id}")
        print(f"To:   {msg.receiver_id}")
        print(f"Subject: {msg.subject}")
        print(f"Time: {msg.timestamp}")
        print("Body:")
        print(msg.body)
    print("--------------------------------------------------")




def view_sent_items(server: Email_server) -> None:
    try:
        user_id = int(input("User ID to view sent items: ").strip())
    except ValueError:
        print("User ID must be an integer.")
        return

    mailbox = server.mailboxes.get(user_id)
    if mailbox is None:
        print("No mailbox found for that user.")
        return


    sent = mailbox.sent_items

    if not sent:
        print("No sent items.")
        return

    print(f"\nSent items for user {user_id}:")
    for i, msg in enumerate(sent, start=1):
        print("--------------------------------------------------")
        print(f"Message #{i}")
        print(f"From: {msg.sender_id}")
        print(f"To:   {msg.receiver_id}")
        print(f"Subject: {msg.subject}")
        print(f"Time: {msg.timestamp}")
        print("Body:")
        print(msg.body)
    print("--------------------------------------------------")





def process_outbound_queue(server: Email_server) -> None:
    before = len(server.outbound_queue)
    server.process_outbound_queue()
    delivered = before - len(server.outbound_queue)
    print(f"Delivered {delivered} message(s).")


def main() -> None:
    server = create_demo_server()
    print("Demo email server started with 4 demo users.")

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
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
