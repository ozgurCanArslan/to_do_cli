import datetime


class Todo:
    def __init__(
        self,
        task,
        category,
        date=None,
        status=None,
        position=None,
    ):
        self.task = task
        self.category = category
        self.date = date if date is not None else str(datetime.datetime.now())
        self.status = status if status is not None else 1  # 1 = open, 2 = completed
        self.position = position if position is not None else None

    def __repr__(self) -> str:
        return f"({self.task}, {self.category}, {self.date},  {self.status}, {self.position})"
