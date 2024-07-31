import socket
from tkinter import *
from gameboard import BoardClass

class Player2GUI:
    """Class representing Player 2 in the Tic-Tac-Toe game."""

    def __init__(self):
        """Initialize Player2 object."""

        self.info = None
        self.board = None
        self.username = None

        self.window = Tk()
        self.window.title("Tic-Tac-Toe - Player 2")
        self.window.config(bg='pink')

        self.IP_label = Label(self.window, text="Enter the IP address:",bg='skyblue')
        self.IP_entry = Entry(self.window,bg='skyblue')

        self.port_label = Label(self.window, text="Enter the port to use:",bg='skyblue')
        self.port_entry = Entry(self.window,bg='skyblue')

        self.username_label = Label(self.window, text="Enter your username:",bg='skyblue')
        self.username_entry = Entry(self.window,bg='skyblue')

        self.connect_button = Button(self.window, text="Connect", command=self.connect_to_player1,bg='skyblue')

        self.current_player_label = Label(self.window, text="Current Player: ",bg='skyblue')
        self.current_player_display = Label(self.window, text="",bg='skyblue')
        self.text_box_display = Label(self.window, text="",bg='skyblue')

        self.create_board_buttons()
        self.setup_layout()

    def create_board_buttons(self):
        """Create the buttons for the Tic-Tac-Toe board."""
        self.buttons = []
        for row in range(3):
            row_buttons = []
            for col in range(3):
                button = Button(self.window, text=" ", width=10, height=5,
                                command=lambda r=row, c=col: self.handle_button_click(r, c))
                button.grid(row=row, column=col + 3)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def setup_layout(self):
        """Set up the layout of the GUI."""
        self.IP_label.grid(row=0, column=0, padx=10, pady=5)
        self.IP_entry.grid(row=0, column=1, padx=10, pady=5)

        self.port_label.grid(row=1, column=0, padx=10, pady=5)
        self.port_entry.grid(row=1, column=1, padx=10, pady=5)

        self.username_label.grid(row=2, column=0, padx=10, pady=5)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)
        self.connect_button.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

        self.current_player_label.grid(row=6, column=0, padx=10, pady=5)
        self.current_player_display.grid(row=6, column=1, padx=10, pady=5)
        self.text_box_display.grid(row=7, column=1, padx=10, pady=5)

    def connect_to_player1(self):
        """
        Connect to Player 1 using the provided IP address and port.

        Args:
            None.

        Returns:
            None
        """

        IP_address = self.IP_entry.get()
        port = int(self.port_entry.get())
        self.info = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.info.bind((IP_address, port))
        self.info.listen(1)
        self.text_box_display.config(text=f"Waiting for other player to connect...")
        self.conn, addr = self.info.accept()
        player1_username = self.conn.recv(1024).decode()
        self.text_box_display.config(text=f"Connected!")
        self.username = self.username_entry.get()
        self.conn.send(self.username.encode())
        self.board = BoardClass(player1_username, self.username)
        self.current_player_display.config(text=self.board.player1)
        self.window.update()
        self.wait_for_move()

    def handle_button_click(self, row, col):
        """
        Handle the button click on the Tic-Tac-Toe board buttons.

        Args:
            row (int): The row number of the clicked button.
            col (int): The column number of the clicked button.

        Returns:
            None
        """

        self.window.update()
        if self.username != self.board.player2:
            self.text_box_display.config(text="It's not your turn!")
            return
        if self.board.board[row][col] != " ":
            self.text_box_display.config(text="Invalid move: The spot is already taken.")
            return
        self.board.updateGameBoard(row, col, self.username)
        self.update_button_text(row, col, self.username)
        self.current_player_display.config(text=self.board.player1)
        self.conn.send(f"{row},{col}".encode())
        self.window.update()
        self.check_game_over()
        self.wait_for_move()

        if self.board.isWinner(self.board.player1):
            self.wait_for_play_again()

    def wait_for_move(self):
        """
        Wait for the move from Player 1 and update the game state.

        Args:
            None.

        Returns:
            None
        """

        self.window.update()
        player1_move = self.conn.recv(1024).decode()

        if self.check_winner() == 'X':
            self.text_box_display.config(text=f"Game Over! {self.board.player1} wins!")
            self.wait_for_play_again()

        if player1_move == 'Play again':
            self.board.resetGameBoard()
            self.board.updateGamesPlayed()
            self.create_board_buttons()
        elif player1_move == 'Fun times':
            self.board.updateGamesPlayed()
            self.text_box_display.config(text=self.board.computeStats())
            return
        row, col = map(int, player1_move.split(","))
        self.board.updateGameBoard(row, col, self.board.player1)
        self.update_button_text(row, col, self.board.player1)
        self.current_player_display.config(text=self.username)
        self.window.update()

    def check_winner(self):
        """
        Check if there is a winner on the Tic-Tac-Toe board by going through the buttons.

        Args:
            None.

        Returns:
            str or None: The symbol of the winning player ('X' or 'O') if there is a winner,
                         None if there is no winner yet.
        """

        for row in self.buttons:
            if row[0]['text'] == row[1]['text'] == row[2]['text'] != ' ':
                return row[0]['text']

        for col in range(3):
            if self.buttons[0][col]['text'] == self.buttons[1][col]['text'] == self.buttons[2][col]['text'] != ' ':
                return self.buttons[0][col]['text']

        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != ' ':
            return self.buttons[0][0]['text']
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != ' ':
            return self.buttons[0][2]['text']

        return None

    def update_button_text(self, row, col, text):
        """
        Update the text and appearance of the button on the Tic-Tac-Toe board.

        Args:
            row (int): The row index of the button.
            col (int): The column index of the button.
            text (str): The new text to be shown on the button.

        Returns:
            None
        """

        if text == self.board.player2:
            self.buttons[row][col].config(text='O', bg='red')
            self.buttons[row][col].config(state=DISABLED)
        elif text == self.board.player1:
            self.buttons[row][col].config(text='X', bg='green')
            self.buttons[row][col].config(state=DISABLED)

    def check_game_over(self):
        """
        Check if the game is over.

        Returns:
            None
        """

        if self.board.isWinner(self.board.player1):
            winner = self.board.player1
            self.text_box_display.config(text=f"Game Over! {winner} wins!")
            self.wait_for_play_again()

        elif self.board.isWinner(self.board.player2):
            winner = self.board.player2
            self.text_box_display.config(text=f"Game Over! {winner} wins!")
            self.wait_for_play_again()

        elif self.board.boardIsFull():
            self.text_box_display.config(text="Game Over! It's a tie!")
            self.wait_for_play_again()

    def wait_for_play_again(self):
        """
        Wait for the play again command from Player 1.

        Returns:
            None
        """

        self.play_again = self.conn.recv(1024).decode()
        if self.play_again == "Play again":
            self.board.resetGameBoard()
            self.board.updateGamesPlayed()
            self.create_board_buttons()

        elif self.play_again == "Fun times":
            self.board.updateGamesPlayed()
            self.text_box_display.config(text=self.board.computeStats())

    def run(self):
        """
        Run the mainloop.

        Args:
            None.

        Returns:
            None
        """

        self.window.mainloop()


if __name__ == "__main__":
    player2 = Player2GUI()
    player2.run()