from typing import List

LIMIT = 250


def calculate_pagination_offsets(cnt: int) -> List:
    # cnt = 26854
    offsets = []
    current_pos = 0
    while current_pos < cnt:
        offset = current_pos
        current_pos += LIMIT
        offsets.append(offset)
    return offsets
