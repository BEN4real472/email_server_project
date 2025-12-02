import pytest
import random
import string

from email_server.email_server import Email_server


@pytest.mark.slow
def test_email_server_handles_500_users_and_many_messages():
    """
    Scalability test:
    - 500 users
    - 5,000 messages between random users
    """
    server = Email_server(capacity=4096)

    # Create 500 users
    for i in range(500):
        server.add_user(i, f"User{i}", f"user{i}@example.com")

    # Send 5,000 messages between random users
    for i in range(5000):
        sender = random.randint(0, 499)
        receiver = random.randint(0, 499)
        subject = f"LoadTest{i}"
        body = "".join(random.choices(string.ascii_letters, k=50))
        server.send_email(sender, receiver, subject, body)

    server.process_outbound_queue()

    # Spot-check inbox retrieval
    for uid in [0, 100, 250, 400]:
        inbox = server.get_inbox(uid, sort_by="time")
        assert isinstance(inbox, list)
