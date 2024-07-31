class BoardClass:
    """A Tic-Tac-Toe game board."""
    
    def __init__(self, player1, player2):
        """Initalize the Boardclass object.

        Args:
            player1 (str): the name of player1.
            player2 (str): the name of player2.
        """

        self.player1 = player1
        self.player2 = player2
        self.last_player = None
        self.wins = {'player1' : 0, 'player2' : 0}
        self.losses = {'player1' : 0, 'player2' : 0}
        self.ties = 0
        self.board = [[" ", " ", " ",], [ " ", " ", " ",], [ " ", " ", " ",]]
        self.games = 0
    
    def updateGamesPlayed(self):
        """Update the number of games played."""
        
        self.games = self.games + 1
    
    def resetGameBoard(self):
        """Reset the game board."""
        
        self.board = [[" ", " ", " ",], [ " ", " ", " ",], [ " ", " ", " ",]]
    
    def updateGameBoard(self, row, col, player):
        """Update the game board with moves.
        
        Args:
            row (int): the number of row of the move.
            col (int): the number of column of the move.
            player (str): The player making the move.
        """
        
        self.board[row][col] = player
        self.last_player = player
        

    def isWinner(self, player):
        """Check if the player has won the game.
        
        Args:
            player (str): check which player it is.
        
        Returns:
            bool: True if the player has won, False otherwise.
        """
        
        for row in range(3):
            if self.board[row][0] == player and self.board[row][1] == player and self.board[row][2] == player:
                if player == self.player1:
                    self.wins['player1'] += 1
                    self.losses['player2'] += 1
                    return True
                elif player == self.player2:
                    self.wins['player2'] += 1
                    self.losses['player1'] += 1
                    return True
                    
        for col in range(3):
            if self.board[0][col] == player and self.board[1][col] == player and self.board[2][col] == player:
                if player == self.player1:
                    self.wins['player1'] += 1
                    self.losses['player2'] += 1
                    return True
                
                elif player == self.player2:
                    self.wins['player2'] += 1
                    self.losses['player1'] += 1
                    return True
                    
        if (self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player):
            if player == self.player1:
                self.wins['player1'] += 1
                self.losses['player2'] += 1
                return True
            
            elif player == self.player2:
                self.wins['player2'] += 1
                self.losses['player1'] += 1
                return True
            
        elif (self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player):
            if player == self.player1:
                self.wins['player1'] += 1
                self.losses['player2'] += 1
                return True
            
            elif player == self.player2:
                self.wins['player2'] += 1
                self.losses['player1'] += 1
                return True
        
        return False

    
    def boardIsFull(self):
        """Check to see if the game board is full.
        
        Returns:
            bool: True if the board is full, False otherwise.
        """
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    return False
                
        self.ties = self.ties + 1
        return True
    
    def computeStats(self):
        """Compute game statistics and return as a string.
        
        Returns:
            str: Computed stats.
            
        """

        stats = f"Player 1: {self.player1}\n"
        stats += f"Player 2: {self.player2}\n"
        stats += f"Last player: {self.last_player}\n"
        stats += f"Number of games played: {self.games}\n"
        stats += f"{self.player1}'s wins: {self.wins['player1']}\n"
        stats += f"{self.player1}'s losses: {self.losses['player1']}\n"
        stats += f"{self.player2}'s wins: {self.wins['player2']}\n"
        stats += f"{self.player2}'s losses: {self.losses['player2']}\n"
        stats += f"Number of ties: {self.ties}\n"

        return stats
    
    def printStats(self):
        """Print game statistics."""
        
        print(f"player1: ",{self.player1})
        print(f"player2: ",{self.player2})
        print(f'Last player: ',{self.last_player})
        print(f'number of games: ',{self.games})
        print(f"player1's number of wins: ",{self.wins['player1']})
        print(f"player1's number of losses: ", {self.losses['player1']})
        print(f"player2's number of wins: ", {self.wins['player2']})
        print(f"player2's number of losses: ", {self.losses['player2']})
        print(f'number of ties: ',{self.ties})
        
        
        