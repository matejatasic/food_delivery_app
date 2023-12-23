import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells.copy() if len(self.cells) == self.count else None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells.copy() if len(self.cells) == 0 else None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if not cell in self.cells:
            return None
        
        self.cells.remove(cell)
        self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if not cell in self.cells:
            return None

        self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        self.mark_move_made(cell)

        self.mark_safe(cell)
        
        neigboring_cells = self.get_neighbouring_cells(cell)
        cells_with_unknown_state = self.get_cells_with_unknown_state(neigboring_cells)
    
        new_sentence = Sentence(cells=cells_with_unknown_state, count=count)
        self.add_new_sentence(new_sentence)

        self.mark_new_fields()
        self.infer_new_sentences(new_sentence)

    def mark_move_made(self, cell):
        self.moves_made.add(cell)

    def get_neighbouring_cells(self, cell):
        row = cell[0]
        column = cell[1]
        neighboring_cells = set()

        # get neighboring cells for the row before
        if row - 1 >= 0:
            if column - 1 >= 0:
                neighboring_cells.add((row-1, column-1))
            if column + 1 < self.width:
                neighboring_cells.add((row-1, column+1))

            neighboring_cells.add((row-1, column))

        # get neighbouring cells in the same row
        if column - 1 >= 0:
            neighboring_cells.add((row, column-1))
        if column + 1 < self.width:
                neighboring_cells.add((row, column+1))

        # get neighboring cells for the row after
        if row + 1 < self.height:
            if column - 1 > 0:
                neighboring_cells.add((row+1, column-1))
            if column + 1 < self.width:
                neighboring_cells.add((row+1, column+1))

            neighboring_cells.add((row+1, column))
    
        return set(neighboring_cells)
    
    def get_cells_with_unknown_state(self, cells):
        return {cell for cell in cells if not cell in self.safes and not cell in self.mines and not cell in self.moves_made}

    def add_new_sentence(self, sentence):
        if len(sentence.cells) == 0:
            return None
        
        self.knowledge.append(sentence)

    def mark_new_fields(self):
        for sentence in self.knowledge:
            known_safes = sentence.known_safes()
            known_mines = sentence.known_mines()

            if not known_safes and not known_mines:
                continue

            self.mark_multiple_safes(known_safes)
            self.mark_multiple_mines(known_mines)

    def infer_new_sentences(self, new_sentence):
        for sentence in self.knowledge:
            if sentence == new_sentence or not sentence.cells.issubset(new_sentence.cells) or not new_sentence.cells.issubset(sentence.cells):
                continue
            
            if sentence.cells.issubset(new_sentence.cells):
                new_cells = new_sentence.cells - sentence.cells
                new_count = new_sentence.count - sentence.count
                inferred_sentence = Sentence(cells=new_cells, count=new_count)
                
                self.mark_multiple_safes(inferred_sentence.known_safes())
                self.mark_multiple_mines(inferred_sentence.known_mines())

                continue
            
            new_cells = sentence.cells - new_sentence.cells
            new_count = sentence.count - new_sentence.count
            inferred_sentence = Sentence(cells=new_cells, count=new_count)
            
            self.mark_multiple_safes(inferred_sentence.known_safes())
            self.mark_multiple_mines(inferred_sentence.known_mines())

    def mark_multiple_safes(self, fields):
        if not fields:
            return None
       
        for field in fields:
            self.mark_safe(field)

    def mark_multiple_mines(self, fields):
        if not fields:
            return None

        fields_copy = fields.copy()
        
        for field in fields_copy:
            self.mark_mine(field)            

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        moves_left = self.safes - self.moves_made

        if not moves_left:
            return None

        move = moves_left[random.randint(0, len(self.safes) - 1)]

        return move
            
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        is_game_over = self.width * self.height == len(self.moves_made) + len(self.mines)

        if is_game_over:
            return None

        moves_made_list = list(self.moves_made)
        known_mines_list = list(self.mines)
        move = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        
        while move in moves_made_list or move in known_mines_list:
            move = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        return move
