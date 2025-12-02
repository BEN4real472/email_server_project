import pytest
from email_server.email_server import Email_server


def test_add_user_and_retrieve():
    server = Email_server(capacity=16)

    server.add_user(1, "Alice", "alice@example.com")
    server.add_user(2, "Bob", "bob@example.com")

    user1 = server.get_user(1)
    user2 = server.get_user(2)

    assert user1 is not None
    assert user2 is not None
    assert user1.name == "Alice"
    assert user2.email_address == "bob@example.com"


def test_send_email_places_message_in_queue():
    server = Email_server(capacity=16)
    server.add_user(1, "Alice", "alice@example.com")
    server.add_user(2, "Bob", "bob@example.com")

    server.send_email(1, 2, "Hello", "Message body")
    assert len(server.outbound_queue) == 1


def test_process_outbound_queue_delivers_email():
    server = Email_server(capacity=16)
    server.add_user(1, "Alice", "alice@example.com")
    server.add_user(2, "Bob", "bob@example.com")

    server.send_email(1, 2, "Test", "Hello Bob")
    server.process_outbound_queue()

    inbox = server.get_inbox(2, sort_by="time")

    assert len(inbox) == 1
    assert inbox[0].subject == "Test"
    assert inbox[0].body == "Hello Bob"
    assert inbox[0].sender_id == 1
    assert inbox[0].receiver_id == 2


def test_inbox_sorted_by_time_is_monotonic():
    server = Email_server(capacity=16)
    server.add_user(1, "Alice", "alice@example.com")
    server.add_user(2, "Bob", "bob@example.com")

    for i in range(5):
        server.send_email(1, 2, f"Msg {i}", f"Body {i}")
    server.process_outbound_queue()

    inbox = server.get_inbox(2, sort_by="time")
    timestamps = [m.timestamp for m in inbox]

    assert len(inbox) == 5
    assert timestamps == sorted(timestamps)

