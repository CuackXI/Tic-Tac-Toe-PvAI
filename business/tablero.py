"""Estandarización de tableros representables con una matriz."""

from abc import ABC, abstractmethod

class Tablero(ABC):
    """Estandarización de tableros."""

    @abstractmethod
    def construir_tablero(self):
        """Metodo que instancia la matriz y la construye."""

    @abstractmethod
    def __iter__(self):
        """Iterador del tablero."""

    @abstractmethod
    def __eq__(self, tablero):
        """Compara si dos tableros son iguales.

        Args:
            tablero (Tablero): El tablero a comparar.

        Raises:
            TypeError: Si el tablero a comparar no es de tipo tablero.

        Returns:
            bool: La igualdad de los tableros.
        """

    @abstractmethod
    def coordenadas_validas(self, x, y):
        """Determina si ciertas cordenadas son validas dentro de la matriz del tablero.

        Args:
            x (int): La coordenada x
            y (int): La coordenada y

        Returns:
            bool: Si es valida la coordenada o no.
        """

    @abstractmethod
    def insertar_elemento(self, x, y, elemento):
        """Inserta un elemento en el tablero.

        Args:
            x (int): Coordenada x
            y (int): Coordenada y
            any: Elemento
        """

    @abstractmethod
    def elemento_coordenadas(self, x, y):
        """Devuelve el objeto en determinada coordenada.

        Args:
            x (int): La coordenada x
            y (int): La coordenada y
        
        Raises:
            TypeError: Si las coordenadas no son un entero.
            ValueError: Si las coordenadas no son validas.

        Returns:
            _type_: El elemento en esas coordenadas.
        """

    @abstractmethod
    def tablero_lleno(self):
        """Propiedad que determina si el tablero esta lleno.

        Returns:
            bool: Si esta lleno devuelve True
        """

    @abstractmethod
    def check_patrones(self):
        """Chequea por determinados patrones de elementos en la matriz."""