"""Clases para el funcionamiento de un Participante en una partida de Ta-Te-Ti."""

import business.tablero_tateti as tablero_tateti
import business.juego as juego
from abc import ABC, abstractmethod
import random

class Ficha():
    """Ficha insertable en un tablero"""
    def __init__(self, simbolo):
        if not isinstance(simbolo, str):
            raise TypeError("El simbolo debe ser de tipo str o convertible a ese tipo.")
        
        if len(simbolo) > 1 or simbolo == "" or simbolo == " ":
            raise ValueError("La ficha no puede estar vacia o ser mas de 1 caracter.")

        self.__simbolo = str(simbolo)

    def simbolo(self):
        return self.__simbolo

    def __repr__(self) -> str:
        """Representacion de una ficha (usada para la comparacion de fichas)

        Returns:
            str: Representacion de una ficha.
        """
        return f'Ficha({self.__simbolo})'

    def __str__(self) -> str:
        """Representacion en string de la ficha.

        Returns:
            str: El string que representa la ficha.
        """
        return str(self.__simbolo)

    def __hash__(self):
        return hash(self.simbolo())

    def __eq__(self, ficha: "Ficha") -> bool:
        """Compara si dos fichas son iguales.

        Args:
            ficha (Ficha): La ficha a comparar.

        Raises:
            TypeError: Si la 'ficha' por argumento no es de tipo ficha.

        Returns:
            bool: Si es igual o no.
        """
        if ficha is None:
            return False

        if not isinstance(ficha, Ficha):
            raise TypeError(f'No se puede comparar ficha con {type(ficha)}')

        return repr(self) == repr(ficha)

    def __lt__(self, elemento: "Ficha"):
        if elemento is None:
            return False
        if not isinstance(elemento, Ficha):
            raise TypeError(f"No se puede comparar Ficha con {type(elemento)}")
        return self.simbolo() < elemento.simbolo()


class ParticipanteTateti(ABC):
    """Clase base para participantes en el juego de Ta-Te-Ti"""

    def __init__(self):
        self.__nombre = None
        self.__ficha = None

    def nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser un texto.")
        self.__nombre = nombre

    def ficha(self):
        return self.__ficha

    def set_ficha(self, ficha):
        if not isinstance(ficha, Ficha):
            raise TypeError("La ficha debe ser una ficha.")

        self.__ficha = ficha

    @abstractmethod
    def elegir_ficha(self):
        """El jugador elige que ficha usar en caso de que no sea asignada automáticamente con X o O. Devuelve una ficha."""

    @abstractmethod
    def colocar_ficha(self, tablero) -> tuple[str, str]:
        """Realiza su movimiento en la partida de Ta-Te-Ti. Devuelve las coordenadas del movimiento."""

class Jugador(ParticipanteTateti):
    """Jugador que participa en una partida de Ta-Te-Ti"""

    def elegir_ficha(self):
        simbolo = input(f'{self.nombre()}, elegí que ficha vas a usar: ')

        return Ficha(simbolo)

    def colocar_ficha(self, partida: "juego.Tateti"):
        x = input(f'Columna (1 - {partida.tablero().columnas()}): ')
        y = input(f'Fila (1 - {partida.tablero().filas()}): ')

        return x, y
    
class Minimax_AI(ParticipanteTateti):
    """IA que utiliza un algoritmo de busqueda Minimax para elegir siempre la mejor jugada"""
    def __init__(self):
        super().__init__()
        self.set_nombre("AI")
        self.tablero: "tablero_tateti.Tablero" = None
        self.tablero_min_max: "tablero_tateti.Tablero" = None
        self.contador = 0
        self.depth_limit = 0

    def elegir_ficha(self):
        self.set_ficha(Ficha("#"))

    def colocar_ficha(self, partida: "juego.Tateti"):
        self.contador = 0
        if partida.tablero().tablero_vacio():
            move = random.choice(partida.tablero().moves)
        else:
            move = self.best_action(partida)
        return move

    def best_action(self, partida: "juego.Tateti"):
        move_values = []
        self.tablero = partida.tablero().clone()

        self.depth_limit = self.calculate_depth_limit(partida.tablero().dimensiones)

        inmediate_move = self.find_immediate_move(partida)
        if inmediate_move:
            return inmediate_move

        for move in self.tablero.moves:
            x, y = move
            self.tablero.insertar_elemento(x, y, self.ficha())

            value = self.minmax(partida, False, float('-inf'), float('inf'), 0)
            move_values.append((move, value))

            self.tablero.vaciar_celda(x, y)
            
        best_move = max(move_values, key=lambda mv: mv[1])

        return best_move[0]

    def calculate_depth_limit(self, dimensiones: int) -> int:
        return max(3, 8 - dimensiones)

    def find_immediate_move(self, partida: "juego.Tateti"):
        ficha_oponente = partida.jugadores()[1].ficha() if partida.jugadores()[0] == self else partida.jugadores()[0].ficha()

        for move in self.tablero.moves:
            x, y = move
            self.tablero.insertar_elemento(x, y, ficha_oponente)

            if self.tablero.check_patrones(self.ficha(), partida.fichas_seguidas()):
                self.tablero.vaciar_celda(x, y)
                return move

            if self.tablero.check_patrones(ficha_oponente, partida.fichas_seguidas()):
                self.tablero.vaciar_celda(x, y)
                return move
            
            self.tablero.vaciar_celda(x, y)

        return None
    
    def minmax(self, partida: "juego.Tateti", is_maximizing: bool, alpha: float, beta: float, depth: int):
        ficha_oponente = partida.jugadores()[1].ficha() if partida.jugadores()[0] == self else partida.jugadores()[0].ficha()

        if self.tablero.check_patrones(self.ficha(), partida.fichas_seguidas()):
            return 1
        elif self.tablero.check_patrones(ficha_oponente, partida.fichas_seguidas()):
            return -1
        elif self.tablero.tablero_lleno():
            return 0
        
        if depth >= self.depth_limit and (partida.tablero().columnas() > 3 and partida.tablero().filas()):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for move in self.tablero.moves:
                x, y = move
                self.tablero.insertar_elemento(x, y, self.ficha())
                value = self.minmax(partida, False, alpha, beta, depth + 1)
                best_score = max(value, best_score)
                alpha = max(alpha, best_score)

                if beta <= alpha:
                    self.tablero.vaciar_celda(x, y)
                    break

                self.tablero.vaciar_celda(x, y)
            return best_score
        else:
            best_score = float('inf')
            for move in self.tablero.moves:
                x, y = move
                self.tablero.insertar_elemento(x, y, ficha_oponente)
                value = self.minmax(partida, True, alpha, beta, depth + 1)
                best_score = min(value, best_score)
                beta = min(beta, best_score)

                if beta <= alpha:
                    self.tablero.vaciar_celda(x, y)
                    break

                self.tablero.vaciar_celda(x, y)
            return best_score