"""Controladores de terminal para el juego TaTeTi."""

import platform
from os import system
from time import sleep
import juego as juego
import tablero_tateti as tablero_tateti
from tablero import TableroUI

class TaTeTiUI():
    """Controlador de UI en la terminal del juego TaTeTi."""

    def __init__(self, tateti: "juego.Tateti"):
        if not isinstance(tateti, juego.Tateti):
            raise TypeError("Se debe pasar una instancia de juego por parametro.")

        self.__tateti = tateti
        self.__tableroUI = TableroTatetiUI(self.__tateti.tablero())

    def cls(self):
        """Vacia la terminal (solo en windows)."""
        if platform.system() == "Windows":
            system('cls')

    def pantalla_bienvenida(self):
        """Muestra la pantalla de bienvenida"""
        self.cls()
        print("\n\t\t\tTa-Te-Ti\n\t\t      Player VS AI")
        sleep(3)

    def mostrar_reglas_actuales(self):
        """Muestra las reglas actuales del juego de Ta-Te-Ti"""
        print(f'Jugadores: {self.__tateti.cant_jugadores()}')
        print(f'Tablero')
        self.__tableroUI.mostrar_tablero()
        print(f'Fichas seguidas: {self.__tateti.fichas_seguidas()}\n')
        input(f'Presiona enter para volver al menu...')

    def mostrar_error(self, mensaje: str):
        """Usado para mostrar mensajes de error

        Args:
            mensaje (str): El mensaje
        """
        print(mensaje)

    def mostrar_fichas_usadas(self):
        """Usado para mostrar las fichas"""
        simbolos = []
        for ficha in self.__tateti.fichas():
            simbolos.append(str(ficha))

        print(f'Fichas usadas: {simbolos}')

    def mostrar_opciones_menu_principal(self):
        """Muestra las opciones del menu principal, usando las opciones establecidas en la instancia de juego"""
        print("Ta-Te-Ti")
        for i in range(len(self.__tateti.opciones_menu_principal())):
            print(f'{i+1} - {self.__tateti.opciones_menu_principal()[i][0]}')

    def mostrar_titulo_eleccion_nombres(self):
        """Muestra el titulo durante el apartado de eleccion de nombres."""
        print("Eleccion de nombres")

    def mostrar_titulo_cant_jugadores(self):
        """Muestra el titulo durante el apartado de eleccion de cantidad de jugadores que participan en la partida."""
        print("Configuracion: Cantidad de jugadores")

    def mostrar_titulo_tamaño_tablero(self):
        """Muestra el titulo durante el apartado de eleccion del tamaño del tablero."""
        print("Configuracion: Tamaño tablero")

    def mostrar_titulo_fichas_seguidas(self):
        """Muestra el titulo durante el apartado de eleccion de fichas seguidas para ganar (win condition)."""
        print("Configuracion: Fichas seguidas (win condition)")

    def mostrar_opciones_eleccion_jugador_inicial(self):
        """Muestra las opciones para la eleccion del jugador inicial."""
        print("Eleccion de jugador inicial")
        for i in range(len(self.__tateti.jugadores())):
            print(f'{self.__tateti.jugadores()[i].nombre()} ({i+1})')

    def mostrar_tablero(self):
        """Muestra el tablero"""
        self.__tableroUI.mostrar_tablero()

    def mostrar_turno_jugador(self, jugador):
        """Muestra quien debe poner su ficha y la ficha que debe poner."""
        print(f'Turno de {jugador.nombre()} // Ficha: {str(jugador.ficha())}')

    def mensaje_ganador(self):
        """Mensaje que se muestra al ganar la partida"""
        self.cls()
        self.mostrar_tablero()
        print(f'Ganó {self.__tateti.jugador_actual().nombre()}')
        sleep(2)

    def mensaje_empate(self):
        """Mensaje que se muestra al empatar la partida"""
        self.cls()
        self.mostrar_tablero()
        print("Empate")
        sleep(2)

class TableroTatetiUI(TableroUI):
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
