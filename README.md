Email Exchange Server – Data Structures and Algorithms Project
Overview
This project implements a simplified organisational email exchange server designed to support approximately 500 staff members. The system models how data structures and algorithms are used to ensure efficient message delivery, fast inbox retrieval, and scalable performance under high message volumes.
The project focuses on algorithm performance analysis and data structure selection, rather than network-level email protocols.

Key Features
•	Add and manage users
•	Send internal email messages
•	Process outbound message queues
•	Retrieve inbox messages efficiently
•	Sort inbox messages by timestamp or sender
•	Handle high message volumes reliably

System Design
The server is implemented in Python and uses carefully selected data structures to ensure efficiency:
Data Structures Used
Component	Data Structure	Reason
User storage	Hash table (hash map)	O(1) average lookup time
Mailboxes	Hash map + lists	Fast access and organisation
Outbound messages	Queue (linked-list/deque style)	O(1) enqueue/dequeue
Inbox sorting	Merge Sort	Predictable O(n log n) performance

Algorithm Selection Justification
•	Hash tables provide constant-time (O(1)) average-case access for users and mailboxes.
•	Merge Sort is used instead of Bubble Sort because it guarantees O(n log n) performance in all cases.
•	Separate chaining is used for hash map collision resolution to support dynamic workloads.
•	Linked-list-style queues are used to efficiently manage outbound email delivery.
These choices ensure scalability, reliability, and responsiveness.

Project Structure
email_server_project/
├── email_server/
│   ├── email_models.py
│   ├── datastructures.py
│   ├── email_server.py
│   └── cli_email_demo.py
├── tests/
│   ├── test_datastructures.py
│   ├── test_email_server_basic.py
│   └── test_email_server_scalability.py
├── pytest.ini
├── requirements.txt
└── README.md

Running the Project
Install Dependencies
pip install -r requirements.txt
Run the CLI Demo
python email_server/cli_email_demo.py
Run Tests
pytest -vv

Testing
The project includes automated tests to ensure reliability:
•	Empty data structure handling
•	Null and zero-value inputs
•	Large data volumes (up to millions of values)
•	Scalability testing with 500 users
•	Correct queue and sorting behaviour

Technologies Used
•	Python 3.13
•	Pytest
•	Git & GitHub

Academic Context
This project was developed as part of an academic coursework focusing on:
•	Algorithm performance (Big O notation)
•	Data structure selection
•	Scalability and system efficiency
•	Practical application of theoretical concepts

Author
Benjamin Egoro
GitHub: https://github.com/BEN4real472
