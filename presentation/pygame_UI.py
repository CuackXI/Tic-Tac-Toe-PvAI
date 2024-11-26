"""Controladores de terminal para el juego TaTeTi."""

import business.juego as juego
import business.tablero_tateti as tablero_tateti
from presentation.interfaces import IJuegoUI, TableroUI, IMenu
import pygame

class Display():
    def __init__(self, tateti):
        self.__screen = pygame.display.set_mode((400, 400))
        self.__tateti = tateti

    def __draw_menu(self, menu: IMenu):
        for clickable in menu.clickables:
            pygame.draw.rect(self.__screen, clickable.color, clickable.rect)
            surface = clickable.font.render(clickable.text, True, (255, 255, 255))
            self.__screen.blit(surface, (text.x, text.y))

        try:
            for text in menu.texts:
                surface = text.font.render(text.text, True, (255, 255, 255))
                self.__screen.blit(surface, (text.x, text.y))
        except:
            pass

    def render_frame(self, menu: IMenu):
        self.__draw_menu(menu)

        pygame.display.flip()

class TatetiPYGAME_UI(IJuegoUI):
    """Controlador de UI en la terminal del juego TaTeTi."""

    def __init__(self, tateti: "juego.Tateti"):
        if not isinstance(tateti, juego.Tateti):
            raise TypeError("Se debe pasar una instancia de juego por parametro.")

        self.__display = Display(tateti)
        self.__tateti = tateti
        self.__tableroUI = TableroTatetiTerminalUI(self.__tateti.tablero())

    def pantalla_bienvenida(self):
        pass

    def mostrar_error(self, mensaje: str):
        """Usado para mostrar mensajes de error

        Args:
            mensaje (str): El mensaje
        """
        print(mensaje)

    def mostrar_opciones_menu_principal(self):
        print("Ta-Te-Ti")
        for i in range(len(self.__tateti.opciones_menu_principal())):
            print(f'{i+1} - {self.__tateti.opciones_menu_principal()[i][0]}')

    def mostrar_opciones_eleccion_jugador_inicial(self):
        print("Eleccion de jugador inicial")
        for i in range(len(self.__tateti.jugadores())):
            print(f'{self.__tateti.jugadores()[i].nombre()} ({i+1})')

    def mostrar_tablero(self):
        self.__tableroUI.mostrar_tablero()

    def mostrar_turno_jugador(self, jugador):
        print(f'Turno de {jugador.nombre()} // Ficha: {str(jugador.ficha())}')

    def mensaje_ganador(self):
        """Mensaje que se muestra al ganar la partida"""
        self.mostrar_tablero()
        print(f'Ganó {self.__tateti.jugador_actual().nombre()}')

    def mensaje_empate(self):
        """Mensaje que se muestra al empatar la partida"""
        self.mostrar_tablero()
        print("Empate")

class TableroTatetiTerminalUI(TableroUI):
    """Clase que maneja como se muestra el tablero en la terminal."""
    def __init__(self, tablero: "tablero_tateti.TableroTateti") -> None:
        if not isinstance(tablero, tablero_tateti.TableroTateti):
            raise TypeError("El tablero debe ser un tablero de tateti.")

        self.__tablero = tablero

    def mostrar_tablero(self):
        techo = "    "
        for top in range(self.__tablero.columnas()):
            techo += str(top+1) + " "
        print(techo)

        for y in range(self.__tablero.filas()):
            if len(str(y+1)) != 1:
                linea = str(y+1) + " "
            else:
                linea = str(y+1) + "  "
                
            for x in range(self.__tablero.columnas()):
                if self.__tablero.tablero()[y][x] is None:
                    valor = " "
                else:
                    valor = str(self.__tablero.tablero()[y][x])
                if x+1 > 9:
                    valor += " "
                linea += f'|{valor}'
            linea += "|"
            print(linea)