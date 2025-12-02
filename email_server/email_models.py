from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    user_id: int
    name: str
    email_address: str


@dataclass
class Email_message:
    sender_id: int
    receiver_id: int
    subject: str
    body: str
    timestamp: datetime

