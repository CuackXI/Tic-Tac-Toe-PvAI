"""Clases para el funcionamiento del tablero del Ta-Te-Ti"""

from tablero import Tablero
import juego as juego
import jugador

class TableroTateti(Tablero):
    """Tablero cuyo proposito es su uso en juegos de TaTeTi o variantes compatibles"""

    def __init__(self, filas: int, columnas: int) -> None:
        if not isinstance(filas, int) or not isinstance(columnas, int):
            raise TypeError("Las columnas y las filas deben ser numeros enteros.")

        self.__filas = filas
        self.__columnas = columnas
        self.__tablero = None
        self.construir_tablero()

    def construir_tablero(self):
        self.__tablero = []
        
        for i in range(self.__filas):
            # Crea la fila
            self.__tablero.append([])

            for _ in range(self.__columnas):
                # Crea las columnas de la fila
                self.__tablero[i].append(None)

    @property
    def dimensiones(self):
        return (self.__columnas + self.__filas) // 2

    @property
    def moves(self):
        available_moves = []
        for row in range(1, self.__filas + 1):
            for col in range(1, self.__columnas + 1):
                if self.elemento_coordenadas(col, row) is None:
                    available_moves.append((col, row))
        return available_moves

    def tablero(self):
        return self.__tablero

    def filas(self):
        return self.__filas

    def columnas(self):
        return self.__columnas

    def set_tablero(self, tablero):
        self.__tablero = tablero

    def set_filas(self, filas):
        if filas != 3:
            raise ValueError("No implementado")

        self.__filas = filas

    def set_columnas(self, columnas):
        if columnas != 3:
            raise ValueError("No implementado")

        self.__columnas = columnas

    def __iter__(self):
        for fila in self.__tablero:
            for casillero in fila:
                yield casillero

    def tablero_vacio(self) -> bool:
        for elemento in self:
            if elemento is not None:
                return False
        return True

    def tablero_lleno(self) -> bool:
        for elemento in self:
            if elemento is None:
                return False
        return True

    def __eq__(self, tablero: "TableroTateti") -> bool:
        if not isinstance(tablero, TableroTateti):
            raise TypeError(f'No se puede comparar tablero de tateti con {type(tablero)}')

        return self.__tablero == tablero.tablero()

    def coordenadas_validas(self, x: int, y: int) -> bool:
        return x > self.__columnas or x < 1 or y > self.__filas or y < 1

    def insertar_elemento(self, x: int, y: int, elemento: "jugador.Ficha"):
        if not isinstance(x, int) or not isinstance(y, int) or not isinstance(elemento, jugador.Ficha):
            raise TypeError("Las coordenadas deben ser numeros y la ficha debe ser una ficha.")

        if self.coordenadas_validas(x, y):
            raise ValueError("Coordenadas fuera de rango")

        if isinstance(self.__tablero[y-1][x-1], jugador.Ficha):
            raise OcupadoError(f'Casillero ocupado ({x}, {y})')

        self.__tablero[y-1][x-1] = elemento

    def vaciar_celda(self, x: int, y: int):
        self.__tablero[y-1][x-1] = None

    def elemento_coordenadas(self, x: int, y: int):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("Las coordenadas deben ser numeros y la ficha debe ser una ficha.")
        if self.coordenadas_validas(x, y):
            raise ValueError("Coordenadas fuera de rango.")

        return self.__tablero[y-1][x-1]
    
    def check_patrones(self, ficha: "jugador.Ficha", fichas_seguidas: int) -> bool:
        # Busca alguno de los patrones del tateti
        if self.patron_filas(ficha, fichas_seguidas) or self.patron_columnas(ficha, fichas_seguidas) or self.patron_diagonales(ficha, fichas_seguidas):
            return True

        # Si no encuentra ningun patrón que cumpla con lo pedido
        return False
    
    def patron_filas(self, ficha, fichas_seguidas) -> bool:
        """Busca por una determinada ficha en un patron horizontal"""

        # Horizontales
        for y in range(self.__filas):
            for x in range(self.__columnas - fichas_seguidas + 1):
                encontrado = True
                for i in range(fichas_seguidas):
                    if self.elemento_coordenadas(x + i + 1, y + 1) != ficha:
                        encontrado = False
                        break
                if encontrado:
                    return True

    def patron_columnas(self, ficha, fichas_seguidas) -> bool:
        """Busca por una determinada ficha en un patron vertical"""

        # Verticales
        for x in range(self.__columnas):
            for y in range(self.__filas - fichas_seguidas + 1):
                encontrado = True
                for i in range(fichas_seguidas):
                    if self.elemento_coordenadas(x + 1, y + i + 1) != ficha:
                        encontrado = False
                        break
                if encontrado:
                    return True
                
    def patron_diagonales(self, ficha, fichas_seguidas) -> bool:
        """Busca por una determinada ficha en un patron diagonal"""

        # Izquierda - Derecha
        for y in range(self.__filas - fichas_seguidas + 1):
            for x in range(self.__columnas - fichas_seguidas + 1):
                encontrado = True
                for i in range(fichas_seguidas):
                    if self.elemento_coordenadas(x + i + 1, y + i + 1) != ficha:
                        encontrado = False
                        break
                if encontrado:
                    return True
                
        # Derecha - Izquierda
        for y in range(fichas_seguidas - 1, self.__filas):
            for x in range(self.__columnas - fichas_seguidas + 1):
                encontrado = True
                for i in range(fichas_seguidas):
                    if self.elemento_coordenadas(x + i + 1, y - i + 1) != ficha:
                        encontrado = False
                        break
                if encontrado:
                    return True

    def clone(self):
        """Creates a copy of the current board"""
        cloned_tablero = TableroTateti(self.__filas, self.__columnas)
        cloned_tablero.set_tablero([row[:] for row in self.__tablero])
        return cloned_tablero

class OcupadoError(Exception):
    pass
