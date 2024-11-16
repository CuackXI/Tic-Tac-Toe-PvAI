"""Juego de tablero 'Ta-Te-Ti'"""

from tablero_tateti import *
from jugador import *
from tateti_ui import TaTeTiUI

class Tateti():
    """Juego de tateti Player VS AI donde la IA siempre gana o empata."""
    def __init__(self):
        # Configuracion predeterminada
        self.__tablero = TableroTateti(3, 3)
        self.__cant_jugadores = 2
        self.__fichas_seguidas = 3

        self.__corriendo = True
        self.__UI = TaTeTiUI(self)
        self.__jugadores = []
        self.__fichas = []
        self.__fichas_default = [Ficha("X"), Ficha("O")]
        self.__indice_turno = 0

        # Opciones de menu
        self.__opciones_menu_principal = [("Jugar", self.__jugar), ("Salir", self.__salir_del_juego)]

    @property
    def __jugador_actual(self):
        return self.__jugadores[self.__indice_turno]
    
    # Getters
    def tablero(self):
        return self.__tablero

    def jugadores(self):
        return self.__jugadores

    def indice_turno(self):
        return self.__indice_turno

    def cant_jugadores(self):
        return self.__cant_jugadores

    def opciones_menu_principal(self):
        return self.__opciones_menu_principal
    
    def fichas(self):
        return self.__fichas

    def fichas_seguidas(self):
        return self.__fichas_seguidas

    def jugador_actual(self):
        return self.__jugador_actual

    # Setters
    def __set_indice_turno(self, indice):
        if indice < 0 or indice > len(self.__jugadores)-1:
            raise IndexError(f'Indice fuera de rango (1 - {len(self.__jugadores)})')

        self.__indice_turno = indice

    # Métodos
    @classmethod
    def iniciar(clase):
        """Inicia el juego de Ta-Te-Ti"""
        tateti = clase()
        tateti.__UI.pantalla_bienvenida()
        tateti.__menu()

    def __menu(self, mensaje_error = None):
        """Etapa donde se recorre el menu principal"""
        while self.__corriendo:
            self.__UI.cls()
            self.__UI.mostrar_opciones_menu_principal()

            # Si se generó un mensaje de error, se muestra
            if mensaje_error is not None:
                self.__UI.mostrar_error(mensaje_error)

            eleccion = input('Opcion: ')

            try:
                if int(eleccion) > 0: #Evita que se utilicen indices negativos
                    # Ejecuta el método del menu principal
                    self.__opciones_menu_principal[int(eleccion)-1][1]()
                else:
                    raise IndexError
            except ValueError:
                self.__menu(mensaje_error = f'Opción no válida ({eleccion} no es un número)')
            except IndexError:
                # Número fuera de rango
                self.__menu(mensaje_error = f'Opción no válida ({eleccion} no esta en (1 - {len(self.__opciones_menu_principal)}))')

    def __jugar(self):
        """Inicia un partida"""
        try:
            self.__set_up_inicial()

            while True:
                self.__realizar_movimiento(self.__jugador_actual)

                # Si hay ganador
                if self.__check_ganador(self.__jugador_actual):
                    self.__UI.mensaje_ganador()
                    self.__reset_tablero()
                    break

                # Si hay empate
                if self.__check_empate():
                    self.__UI.mensaje_empate()
                    self.__reset_tablero()     
                    break

                self.__siguiente_jugador()

            # Si termina la partida
            self.__menu()
        except KeyboardInterrupt:
            self.__menu()
        except Exception as e:
            print(f'ERROR: {e}')

    def __salir_del_juego(self):
        """Termina la ejecucion del juego"""
        self.__UI.cls()
        self.__corriendo = False

    def __set_up_inicial(self):
        """Establece un estado inicial para empezar la partida"""
        self.__reset_jugadores()
        self.__reset_fichas()
        self.__settear_nombres()
        self.__elegir_jugador_inicial()
        self.__settear_fichas()

    def __reset_jugadores(self):
        """Se resetean los jugadores"""
        self.__jugadores.clear()
        self.__jugadores.append(Minimax_AI())
        # self.__jugadores.append(Minimax_AI())

    def __reset_tablero(self):
        """Se resetea el tablero"""
        self.__tablero.construir_tablero()

    def __reset_fichas(self):
        """Se resetean las fichas"""
        self.__fichas = self.__fichas_default

    def __settear_nombres(self):
        self.__jugadores.append(Jugador())
        nombre = "Player"

        self.__jugadores[1].set_nombre(nombre)
        pass

    def __elegir_jugador_inicial(self, mensaje_error = None):
        """Etapa de eleccion del jugador inicial"""
        self.__UI.cls()
        self.__UI.mostrar_opciones_eleccion_jugador_inicial()
        
        # Si hay un mensaje de error se muestra
        if mensaje_error is not None:
            self.__UI.mostrar_error(mensaje_error)
            
        jugador_inicial = input('Elige un jugador para que comience la partida: ')

        try:
            self.__set_indice_turno(int(jugador_inicial) - 1)
        
        except ValueError:
            # Si no se ingresa un número
            self.__elegir_jugador_inicial(mensaje_error = f'Se debe ingresar un número ({jugador_inicial})')
        except IndexError as Error:
            # Si el indice no es válido
            self.__elegir_jugador_inicial(mensaje_error = Error)

    def __settear_fichas(self):
        """Setteo de fichas X y O a los primeros 2 jugadores"""
        self.__UI.cls()

        indice_ficha = 0
        indice_jugador = 0

        try:
            # Va desde jugador inicial hasta el final de la lista
            for i in range(self.__indice_turno, len(self.__jugadores)):
                self.__jugadores[i].set_ficha(self.__fichas[indice_ficha])
                indice_ficha += 1
                indice_jugador = i

            # Va desde el inicio de la lista hasta el jugador inicial
            for i in range(self.__indice_turno):
                self.__jugadores[i].set_ficha(self.__fichas[indice_ficha])
                indice_ficha += 1
                indice_jugador = i

        except IndexError:
            # Cuando se acaban las fichas predeterminadas
            self.__eleccion_fichas(indice_jugador + 1)

    def __realizar_movimiento(self, jugador: "ParticipanteTateti", mensaje_error=None):
        """Etapa donde un participante realiza su movimiento.

        Args:
            jugador (tablero_tateti.ParticipanteTateti): El participante que tiene su turno.
        """

        self.__UI.cls()
        self.__UI.mostrar_tablero()
        self.__UI.mostrar_turno_jugador(jugador)

        # Si hay un mensaje de error se muestra
        if mensaje_error is not None:
            self.__UI.mostrar_error(mensaje_error)

        # Se devuelven las elecciones del jugador
        x, y = jugador.colocar_ficha(self)

        try:
            self.__tablero.insertar_elemento(int(x), int(y), jugador.ficha())

        except TypeError as Error:
            # Si se detecta un tipo inválido
            self.__realizar_movimiento(jugador, mensaje_error = Error)

        except ValueError as Error:
            # Coordenadas fuera de rango
            self.__realizar_movimiento(jugador, mensaje_error = f'Coordenadas inválidas ({x}, {y})')

        except OcupadoError as Error:
            # Si el casillero está ocupado
            self.__realizar_movimiento(jugador, mensaje_error = Error)

    def __check_ganador(self, jugador: "ParticipanteTateti"):
        """Chequea si un jugador ganó o no"""
        return self.__tablero.check_patrones(jugador.ficha(), self.__fichas_seguidas)

    def __check_empate(self):
        """Chequea si hay empate"""
        return self.__tablero.tablero_lleno()
    
    def __siguiente_jugador(self):
        """Le da el turno al siguiente jugador"""
        self.__indice_turno += 1
        if self.__indice_turno == len(self.__jugadores):
            self.__indice_turno = 0

        self.__UI.cls()