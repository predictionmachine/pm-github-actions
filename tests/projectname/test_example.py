from typing import List

import pytest

from projectname.example import UserId, listify


@pytest.mark.parametrize("user_id, expected_val", [(UserId(1), [UserId(1)])])
def test_listify(user_id: UserId, expected_val: List[UserId]) -> None:
    assert listify(user_id) == expected_val
