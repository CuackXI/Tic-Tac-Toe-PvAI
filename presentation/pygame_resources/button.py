from presentation.interfaces import IButton
import pygame

class Button(IButton):
    def __init__(self, x, y, width: int, height: int, color: pygame.Color, text: str):
        self.__width = width
        self.__height = height
        self.__color = color
        self.__text = text
        self.__rect = pygame.Rect(x, y, self.width, self.height)
        self.__clicked = False

    @property
    def clicked(self) -> bool:
        return self.__clicked

    @property
    def on_hover(self) -> bool:
        pass

    def click_action(self):
        pass

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def color(self) -> pygame.Color:
        return self.__color

    @property
    def text(self) -> str:
        return self.__text