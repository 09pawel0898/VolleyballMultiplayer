import pygame.sprite
from src.core.widgets.widget import Widget
from ..widgets.textbox import TextBox

# unique for each state
class WidgetManager:
    def __init__(self):
        self._widgetsHolder = pygame.sprite.OrderedUpdates()
        self._widgetsDict = {}

    def init_widget(self, name : str, widget : Widget):
        self._widgetsHolder.add(widget)
        self._insert_widget(name,widget)

    def get_widget(self, name: str) -> Widget:
        assert (name in self._widgetsDict)
        return self._widgetsDict[name]

    def update_widgets(self,dt):
        for widget in self._widgetsDict.values():
            widget.update(dt)

    def draw_widgets(self, window):
        self._widgetsHolder.draw(window)

    def _insert_widget(self, key, widget):
        if key not in self._widgetsDict:
            self._widgetsDict[key] = widget

    def deactivate_textboxes_but_one(self, textbox: TextBox):
        for widget in self._widgetsDict.values():
            if isinstance(widget,TextBox):
                widget.enable_input_to_this(False)
        textbox.enable_input_to_this(True)
