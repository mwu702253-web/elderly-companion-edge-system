from dataclasses import dataclass

@dataclass
class Reminder:
    title: str
    time_text: str
    status: str = "pending"
