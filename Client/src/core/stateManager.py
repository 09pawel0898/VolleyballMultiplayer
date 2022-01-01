from enum import Enum
from typing import Callable, Optional, TypeVar
from src.core.stack import Stack
from src.core.state import *


class Action(Enum):
    ADD = 1
    DELETE = 2


class PendingAction:
    def __init__(self, action: Action, state_name: Optional[str] = None) -> None:
        self.action = action
        self.state_name = state_name


class StateManager:
    def __init__(self, context: Context) -> None:
        self._states = Stack()
        self._pending_actions : [PendingAction] = []
        self._context = context
        self._state_constructors : {str,Callable} = {}


    def _create_state(self, state_name: str) -> State:
        assert(state_name in self._state_constructors)
        return self._state_constructors.get(state_name)


    def _do_pending_actions(self) -> None:
        for pending in self._pending_actions:
            if pending.action == Action.ADD:
                self._states.push(self._create_state(pending.state_name)())
            elif pending.action == Action.DELETE:
                self._states.pop()
            if not self._states.is_empty():
                self._states.top().on_awake()
        self._pending_actions.clear()

    def register_state(self,state_name: str, state_type) -> None:
        self._state_constructors[state_name] = lambda : state_type(self,self._context)

    def push_state(self, state_name: str) -> None:
        self._pending_actions.append(PendingAction(Action.ADD,state_name))

    def pop_state(self) -> None:
        if self._states.count() > 0:
            self._pending_actions.append(PendingAction(Action.DELETE))

    def on_render(self) -> None:
        if not self.is_empty():
            self._states.top().on_render()

    def on_update(self, dt: float) -> None:
        if not self.is_empty():
            self._states.top().on_update(dt)
        self._do_pending_actions()

    def on_event(self, events: List[pygame.event.Event]) -> None:
        if not self.is_empty():
            self._states.top().on_event(events)
        self._do_pending_actions()

    def is_empty(self) -> bool:
        return self._states.is_empty()

