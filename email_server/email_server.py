from datetime import datetime, timezone
from typing import List, Optional

from email_server.email_models import User, Email_message
from email_server.datastructures import Hash_map, Mail_queue, merge_sort


class Mailbox:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.inbox: List[Email_message] = []
        self.sent_items: List[Email_message] = []

    def receive_message(self, message: Email_message) -> None:
        self.inbox.append(message)

    def send_message(self, message: Email_message) -> None:
        self.sent_items.append(message)

    def get_sorted_inbox_by_time(self) -> List[Email_message]:
        return merge_sort(self.inbox, key=lambda msg: msg.timestamp)

    def get_sorted_inbox_by_sender(self) -> List[Email_message]:
        return merge_sort(self.inbox, key=lambda msg: msg.sender_id)


class Email_server:
    def __init__(self, capacity: int = 512):
        self.users = Hash_map(capacity=capacity)
        self.mailboxes = Hash_map(capacity=capacity)
        self.outbound_queue = Mail_queue()

    def add_user(self, user_id: int, name: str, email_address: str) -> None:
        user = User(user_id=user_id, name=name, email_address=email_address)
        self.users.put(user_id, user)
        self.mailboxes.put(user_id, Mailbox(user_id=user_id))

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def send_email(self, sender_id: int, receiver_id: int, subject: str, body: str) -> None:
        timestamp = datetime.now(timezone.utc)  # FIXED: timezone-aware and non-deprecated
        message = Email_message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            subject=subject,
            body=body,
            timestamp=timestamp
        )
        self.outbound_queue.enqueue(message)

    def process_outbound_queue(self) -> None:
        while not self.outbound_queue.is_empty():
            message = self.outbound_queue.dequeue()
            if message is None:
                continue

            sender_mailbox = self.mailboxes.get(message.sender_id)
            receiver_mailbox = self.mailboxes.get(message.receiver_id)

            if sender_mailbox is not None:
                sender_mailbox.send_message(message)
            if receiver_mailbox is not None:
                receiver_mailbox.receive_message(message)

    def get_inbox(self, user_id: int, sort_by: str = "time") -> List[Email_message]:
        mailbox = self.mailboxes.get(user_id)
        if mailbox is None:
            return []

        if sort_by == "time":
            return mailbox.get_sorted_inbox_by_time()
        elif sort_by == "sender":
            return mailbox.get_sorted_inbox_by_sender()
        else:
            return list(mailbox.inbox)



