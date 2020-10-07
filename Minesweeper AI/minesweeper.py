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
        Returns a set of all cells in self.cells known to be mines
        (if cells = count) and passes them to mark_mine.
        """
        set_known_mines = set()

        if len(self.cells) == self.count: 
            for cell in self.cells: 
                set_known_mines.add(cell)

            for cell in set_known_mines:
                self.mark_mine(cell)

        return set_known_mines

    def known_safes(self):
        """
        Returns a set of all cells in self.cells known to be safe
        (if count = 0) and passes them to mark_safe.
        """   
        set_known_safes = set()

        if self.count == 0:
            for cell in self.cells: 
                set_known_safes.add(cell)
            
            for cell in set_known_safes:
                self.mark_safe(cell)

        return set_known_safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation 
        given a known mine.
        """
        if (cell) in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation 
        given a known safe cell.
        """
        if (cell) in self.cells:
            self.cells.remove(cell)
                

class MinesweeperAI():
    """
    Minesweeper AI game player
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
        Marks a cell as a mine and updates all knowledge.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe and updates all knowledge.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Adds knowledge when the Minesweeper board provides information
        of a new safe cell and the number of neighboring mines.
        """

        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)
                    
        # Add a new sentence to the AI's knowledge based on the value of `cell` and `count`
        neighboring_cells = set()

        # Loop over all cells within one row and column of cell
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore if cell is safe
                if (i,j) in self.safes:
                    continue

                # Subtract from count if cell is mine and ignore
                if (i,j) in self.mines:
                    count -= 1
                    continue
                
                # Add to set if cell in bounds and it is not known whether it is safe or a mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighboring_cells.add((i, j))

        # If new sentence is empty exit function
        if len(neighboring_cells) == 0:
            return

        # Add new knowledge to knowledge base and, where possible, infer new safe cells or mines   
        new_sentence = Sentence(neighboring_cells, count)
        self.knowledge.append(new_sentence)
        self.safes.update(new_sentence.known_safes())
        self.mines.update(new_sentence.known_mines())

        # Update knowldedge base
        self.update_knowledge()

        # Check for subset sentence relationships
        for sentence in self.knowledge:
            for sentence1 in self.knowledge:
                if sentence != sentence1:
                    
                    # If there is a subset relationship between two sentences
                    if sentence.cells.issubset(sentence1.cells) or sentence1.cells.issubset(sentence.cells):

                        # If sentence is a subset of sentence1, asign new subset cells and corresponding count
                        if sentence.cells.issubset(sentence1.cells):
                            new_set_cells = sentence1.cells - sentence.cells
                            new_set_count = sentence1.count - sentence.count

                        # If sentence1 is a subset of sentence, asign new subset cells and corresponding count
                        if sentence1.cells.issubset(sentence.cells):
                            new_set_cells = sentence.cells - sentence1.cells
                            new_set_count = sentence.count - sentence1.count

                        new_subset_sentence = Sentence(new_set_cells, new_set_count)
                    
                        # If sentence already exists 
                        if new_subset_sentence in self.knowledge: 
                            continue
            
                        # Add new knowledge and, where possible, infer new safe cells or mines   
                        self.knowledge.append(new_subset_sentence)
                        self.safes.update(new_subset_sentence.known_safes())
                        self.mines.update(new_subset_sentence.known_mines())

                        # Update knowldedge base
                        self.update_knowledge()

    def update_knowledge(self):
        """ 
        Updates knowledge base 
        by removing any empty sentences, marking all known mines and safes
        and, where possible, inferring new safe cells or mines. 
        """

        for sentence_i in self.knowledge:
            
            self.safes.update(sentence_i.known_safes())
            self.mines.update(sentence_i.known_mines())

            for cell in self.safes:
                self.mark_safe(cell)
            for cell in self.mines:
                self.mark_mine(cell)

            if len(sentence_i.cells) == 0:
                self.knowledge.remove(sentence_i)
            

          
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        """

        # Set of safe moves
        safe_moves = self.safes - self.moves_made

        # Randomly select safe move
        if len(safe_moves) != 0:
            safe_move = random.choice(list(safe_moves))
            return (safe_move)
        
        #If no safe moves
        else:
            return None

    def make_random_move(self):
        """
        Returns a random move to make on the Minesweeper board.
        """
        
        random_moves = set()

        # Loop over all cells 
        for i in range(0, self.height):
            for j in range(0, self.width):

                # Ignore if cell move is already made
                if (i,j) in self.moves_made:
                    continue

                # Ignore if cell is known to be a mine
                if (i,j) in self.mines:
                    continue

                random_moves.add((i,j))

        # Randomly select move
        if len(random_moves) != 0:
            random_move = random.choice(list(random_moves))
            return (random_move)
        
        # If no random moves available
        else:
            return None