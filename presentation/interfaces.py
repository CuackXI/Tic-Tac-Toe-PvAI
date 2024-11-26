from abc import *
import pygame

class IJuegoUI(ABC):

    @abstractmethod
    def pantalla_bienvenida(self):
        """Muestra la pantalla de bienvenida"""

    @abstractmethod
    def mostrar_opciones_menu_principal(self):
        """Muestra las opciones del menu principal, usando las opciones establecidas en la instancia de juego"""

    @abstractmethod
    def mostrar_opciones_eleccion_jugador_inicial(self):
        """Muestra las opciones para la eleccion del jugador inicial."""

    @abstractmethod
    def mostrar_tablero(self):
        """Muestra el tablero"""

    @abstractmethod
    def mostrar_turno_jugador(self, jugador):
        """Muestra quien debe poner su ficha y la ficha que debe poner."""

    @abstractmethod
    def mensaje_ganador(self):
        """Muestra el mensaje del ganador."""

    @abstractmethod
    def mensaje_empate(self):
        """Muestra el mensaje de empate."""

class IClickable(ABC):
    @property
    @abstractmethod
    def clicked(self) -> bool:
        """Si fue clickeado"""

    @property
    @abstractmethod
    def on_hover(self) -> bool:
        """Si el mouse esta encima"""

    @abstractmethod
    def click_action(self):
        """Realiza la acción"""

class IButton(IClickable):
    @property
    @abstractmethod
    def width(self) -> int:
        pass

    @property
    @abstractmethod
    def height(self) -> int:
        pass
    
    @property
    @abstractmethod
    def color(self) -> pygame.Color:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass

class ITile(IClickable):
    pass

class IFrame(ABC):
    @property
    @abstractmethod
    def clickeables(self) -> list[IClickable]:
        """Lista de todos los elementos clickeables del menu.

        Returns:
            list[IClickable]: Los elementos.
        """

class IMenu(IFrame):
    pass

class TableroUI(ABC):
    """Estandarización de UI de tableros."""

    @abstractmethod
    def mostrar_tablero(self):
        """Muestra el tablero en terminal."""