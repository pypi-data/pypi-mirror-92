class TicTacToe:

    # SYMBOLS FOR players
    SYMBOLS = ["O", "X"]

    # Private variables
    __table = [
        ["_", "_", "_"],
        ["_", "_", "_"],
        ["_", "_", "_"]
    ]


    def init(self):
        pass

    def __draw(self):
        for i in range(3):
            for j in range(3):
                print(self.__table[i][j], end=" ")
            print("")

    def __register_turn(self, player):
        print("Es el turno de la persona", player + 1)

        while True:
            position_x = int(input("Fila: ")) - 1
            position_y = int(input("Columna: ")) - 1

            if position_x > 2 or position_y > 2:
                print("Introduce una fila y/o una columna menor o igual a 3")
                continue

            if self.__table[position_x][position_y] == "_":
                self.__table[position_x][position_y] = self.SYMBOLS[player]
                break
            else:
                print("Esta posicion ya tiene un valor")

    # Check if there are matches in the vector and then it returns
    # True if there is match
    def __does_match(self, array):
        horizontal_result = set(array)

        if len(horizontal_result) == 1 and not '_' in horizontal_result:
            return True

        return False

    def __get_winner(self):

        diagonal_1 = []
        diagonal_2 = []

        for i in range(3):
            # Horizontal
            if self.__does_match(self.__table[i]):
                return True
            else:
                diagonal_1.append(self.__table[i][i])
                diagonal_2.append(self.__table[i][2 - i])


        # Diagonals
        if self.__does_match(diagonal_1):
            return True
       
        if self.__does_match(diagonal_2):
            return True

        vertical_matrix = list(zip(*self.__table))

        for i in range(3):
            # Vertical
            if self.__does_match(vertical_matrix[i]):
                return True

        return False

    def play(self):

        for intent in range(9):
            # getting the turn for the player
            turn = intent % 2
            self.__register_turn(turn)

            # Print the table
            self.__draw()

            if self.__get_winner():
                print(f"El ganador es el jugador {turn + 1}")
                break

        else:
            print("No hay ganadores")
