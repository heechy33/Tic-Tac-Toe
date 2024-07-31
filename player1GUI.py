import socket
from tkinter import *
from gameboard import BoardClass


#10.8.3.57
class Player1GUI:
    """Class representing Player 1 in the Tic-Tac-Toe game."""
    
    
    def __init__(self):
        """Initialize the Player1 object."""
        
        self.info = None
        self.board = None
        self.username = None

        self.window = Tk()
        self.window.title("Tic-Tac-Toe - Player 1")
        self.window.config(bg='pink')

        self.IP_label = Label(self.window, text="Enter the IP address:",bg='skyblue')
        self.IP_entry = Entry(self.window,bg='skyblue')

        self.port_label = Label(self.window, text="Enter the port to use:",bg='skyblue')
        self.port_entry = Entry(self.window,bg='skyblue')

        self.username_label = Label(self.window, text="Enter your username:",bg='skyblue')
        self.username_entry = Entry(self.window,bg='skyblue')

        self.connect_button = Button(self.window, text="Connect", command=self.connect_to_player2,bg='skyblue')
        
        self.text_label = Label(self.window, text='Do you want to play again?',bg='skyblue')
        self.yes_button = Button(self.window, text="Yes", command=self.handle_yes,bg='skyblue')
        self.no_button = Button(self.window, text="No", command=self.handle_no,bg='skyblue')
        
        self.current_player_label = Label(self.window, text="Current Player: ",bg='skyblue')
        self.current_player_display = Label(self.window, text="",bg='skyblue')
        
        self.text_box_display = Label(self.window, text="",bg='skyblue')
        
        self.ask_to_try_again_display = Label(self.window, text="",bg='skyblue')
        self.try_again_yes_button = Button(self.window, text="Yes", command=self.handle_try_again_yes,bg='skyblue')
        self.try_again_no_button = Button(self.window, text="No", command=self.handle_try_again_no,bg='skyblue')
        
        self.create_board_buttons()

        self.setup_layout()

    def create_board_buttons(self):
        """Create the buttons for the Tic-Tac-Toe board."""
        
        self.buttons = []
        for row in range(3):
            row_buttons = []
            for col in range(3):
                button = Button(self.window,text=" ",width=10,height=5,command=lambda r=row, c=col: self.handle_button_click(r, c))
                button.grid(row=row, column=col+3)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def setup_layout(self):
        """Setup the layout of the GUI."""
        
        self.IP_label.grid(row=0, column=0, padx=10, pady=5)
        self.IP_entry.grid(row=0, column=1, padx=10, pady=5)

        self.port_label.grid(row=1, column=0, padx=10, pady=5)
        self.port_entry.grid(row=1, column=1, padx=10, pady=5)

        self.username_label.grid(row=2, column=0, padx=10, pady=5)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)
        self.connect_button.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

        self.current_player_label.grid(row=6, column=0, padx=10, pady=5)
        self.current_player_display.grid(row=6, column=1, padx=10, pady=5)
        self.text_box_display.grid(row=8, column= 1,padx=10, pady=5)
        self.ask_to_try_again_display.grid(row=9,column=0,padx=10, pady=5)

    def connect_to_player2(self):
         """
        Connect to Player 2 using the provided IP address and port.

        Args:
            None.

        Returns:
            None.
        """
         
         IP_address = self.IP_entry.get()
         port = int(self.port_entry.get())
         self.info = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         try:
             self.info.connect((IP_address, port))
             self.send_username()
             player2_username = self.info.recv(1024).decode()
             self.text_box_display.config(text=f"Connected!")
             self.board = BoardClass(self.username, player2_username)
             self.current_player_display.config(text=self.username)

         except:
             self.text_box_display.config(text=f"Connection refused. Unable to connect to other player.")
             self.ask_to_try_again()

    def ask_to_try_again(self):
        """
        Ask the player if they want to try connecting again and display the Yes and No button.

        Args:
            None.

        Returns:
            None.
        """
        self.ask_to_try_again_display.grid(row=9,column=0,padx=10, pady=5)
        self.ask_to_try_again_display.config(text="Do you want to try again?")
        self.try_again_yes_button.grid(row=9, column=1, padx=5, pady=5)
        self.try_again_no_button.grid(row=9, column=2, padx=5, pady=5)

            
    def handle_try_again_no(self):
        """
        Handle the case when the player press No to not try connecting again.

        Args:
            None.

        Returns:
            None.
        """
        self.window.destroy()
        
        
    def handle_try_again_yes(self):
        """
        Handle the case when the player press Yes to try connecting again.

        Args:
            None.

        Returns:
            None.
        """
        self.try_again_yes_button.destroy()
        self.try_again_no_button.destroy()
        self.text_box_display.config(text="Try new information and press connect")

        
    def send_username(self):
        """
        Send the username to the other player.

        Args:
            None.

        Returns:
            None.
        """
        self.username = self.username_entry.get()
        self.info.send(self.username.encode())

        
    def handle_button_click(self, row, col):
        """
        Handle the button click on the Tic-Tac-Toe board buttons.

        Args:
            row (int): The row number of the clicked button.
            col (int): The column number of the clicked button.

        Returns:
            None.
        """
        
        if self.username != self.board.player1:
            self.text_box_display.config(text="It's not your turn!")
        if self.board.board[row][col] == " ":
            self.board.updateGameBoard(row, col, self.username)
            self.update_button_text(row, col, self.username)
            self.current_player_display.config(text=self.board.player2)
            self.info.send(f"{row},{col}".encode())
            self.window.update()
            self.receive_moves_from_player2()

    def receive_moves_from_player2(self):
        """Receive moves from Player 2 and update the game state.

        Args:
            None.

        Returns:
            None.
        """
        
        if self.board.isWinner(self.board.player1):
            self.text_box_display.config(text=f"Game Over! {self.board.player1} wins!")
            self.text_label.grid(row=7, column=0, padx=10, pady=5)
            self.yes_button.grid(row=7, column=1, padx=5, pady=5)
            self.no_button.grid(row=7, column=2, padx=5, pady=5)
            
        elif self.board.isWinner(self.board.player2):
            winner = self.board.player2
            print(f"Game Over! {winner} wins!")
            self.text_label.grid(row=7, column=0, padx=10, pady=5)
            self.yes_button.grid(row=7, column=1, padx=5, pady=5)
            self.no_button.grid(row=7, column=2, padx=5, pady=5)
            
        elif self.board.boardIsFull():
            self.text_box_display.config(text="Game Over! It's a tie!")
            self.text_label.grid(row=7, column=0, padx=10, pady=5)
            self.yes_button.grid(row=7, column=1, padx=5, pady=5)
            self.no_button.grid(row=7, column=2, padx=5, pady=5)
            
        else:
            self.window.update()
            move = self.info.recv(1024).decode()
            player2_row, player2_col = map(int, move.split(","))
            self.board.updateGameBoard(player2_row, player2_col, self.board.player2)
            self.update_button_text(player2_row, player2_col, self.board.player2)
            self.current_player_display.config(text=self.username)
            self.window.update()
            if self.check_winner() == 'O':
                self.text_box_display.config(text=f"Game Over! {self.board.player2} wins!")
                self.board.isWinner(self.board.player2)
                self.text_label.grid(row=7, column=0, padx=10, pady=5)
                self.yes_button.grid(row=7, column=1, padx=5, pady=5)
                self.no_button.grid(row=7, column=2, padx=5, pady=5)
            
                
            
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
            row (int): The row number of the button.
            col (int): The column number of the button.
            text (str): The new text to be shown on the button.
            
        Returns:
            None.
            
        """
        
        if text == self.board.player1:
            self.buttons[row][col].config(text='X', bg='green')
            self.buttons[row][col].config(state=DISABLED)
            
        elif text == self.board.player2:
            self.buttons[row][col].config(text='O', bg='red')
            self.buttons[row][col].config(state=DISABLED)
            
    def handle_yes(self):
        """
        Handle the case when the player press Yes button to play again.

        Args:
            None.

        Returns:
            None.
        """
        self.yes = "Play again"
        self.info.send(self.yes.encode())
        self.board.resetGameBoard()
        self.board.updateGamesPlayed()
        self.create_board_buttons()
        
    def handle_no(self):
        """Handle the case when the player press No to not play again.

        Args:
            None.

        Returns:
            None.
        """
        self.no = "Fun times"
        self.info.send(self.no.encode())
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
    player1 = Player1GUI()
    player1.run()

