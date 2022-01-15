import pygame
import copy
from .roomLabel import RoomLabel
from typing import List
from src.core.util.vector import Vec2
from src.networking.serverRoom.room import RoomHolder,RoomDisplayed
from src.core.resources.texture import Texture

class RoomLabelManager:
    def __init__(self, top_left : Vec2, texture_full : Texture, texture_empty : Texture):
        self._texture_full = texture_full
        self._texture_empty = texture_empty
        self._room_labels : List[RoomLabel] = []
        self._top_left = top_left
        self._active_label = None

    def _add_label(self, label : RoomLabel):
        label.set_position(self._top_left.x,
                           self._top_left.y)
        label.set_callback(self._deactivate_labels_but_one)
        label.set_active(False)
        self._room_labels.append(label)
        self._top_left.y += label.rect.height

    def _deactivate_labels_but_one(self, host: str):
        for label in self._room_labels:
                label.set_active(False)
        for label in self._room_labels:
            if label.host == host:
                label.set_active(True)
                self._active_label = label

    def clear(self):
        self._room_labels.clear()

    def draw(self, window: pygame.Surface):
        for label in self._room_labels:
            label.draw(window)

    def handle_events(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for label in self._room_labels:
                    label.check_for_onclick(label.host)

    def update_labels(self,dt):
        for label in self._room_labels:
            label.update(dt)

    def refresh(self):
        self.clear()
        rooms : List[RoomDisplayed] = RoomHolder.rooms

        for room in rooms:
            if room.people == 0:
                texture = self._texture_empty
                full = False
            else:
                texture = self._texture_full
                full = True
            self._add_label(RoomLabel(texture,room.host_username, room.people, full))

    def get_active_label(self):
        return self._active_label