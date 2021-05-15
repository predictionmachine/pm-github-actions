"""
This file deals with UserId
Provides support for listifying it, eg in service of having thigns as lists
"""
from typing import List, NewType

# Use NewType to create meaningful distinct types, per https://docs.python.org/3/library/typing.html
UserId = NewType("UserId", int)


some_id = UserId(524313)


def listify(user_id: UserId) -> List[UserId]:
    """Returns a list containing the single passed in UserId"""
    return [user_id]
