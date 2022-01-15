from .roomLabel import RoomLabel
from typing import List

class RoomLabelManager:
    def __init__(self):
        self._room_labels : List[RoomLabel] = []

    def add_label(self, label : RoomLabel):
        self._room_labels.append(label)