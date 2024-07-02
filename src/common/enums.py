from enum import StrEnum


class TaskStatus(StrEnum):
    IN_PROGRESS = 'In progress'
    DONE = 'Done'
    ERROR = 'Error'
