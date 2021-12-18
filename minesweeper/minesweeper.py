import copy
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
        if len(self.cells) == self.count:
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
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

    def infer(self):
        # 4 Mark any additional cells as mine or safe
        new_safes = set()
        new_mines = set()
        for sentence in self.knowledge:

            known_mines = copy.deepcopy(sentence.known_mines())
            known_safes = copy.deepcopy(sentence.known_safes())
            # add cells to self.mines or self.safes
            # remove the cells from all sentences in KB and correct the count if mine
            if known_mines is not None:
                for mine in known_mines:
                    self.mark_mine(mine)
                    new_mines.add(mine)

            if known_safes is not None:
                for safe in known_safes:
                    self.mark_safe(safe)
                    new_safes.add(safe)

            if len(sentence.cells) == 0:
                if sentence in self.knowledge:
                    self.knowledge.remove(sentence)

        # 5 If, based on any of the sentences in self.knowledge, new sentences can be inferred (using the subset
        # method described in the Background), then those sentences should be added to the knowledge base as well.
        for sub_sentence, sentence in itertools.permutations(self.knowledge, 2):

            # if the sentence is a subset, create a new sentence
            if sub_sentence.cells.issubset(sentence.cells) and sub_sentence.count != 0 \
                    and len(sub_sentence.cells) != 0:

                # if a sentence was duplicated during the previous step - remove the duplicate
                if len(sub_sentence.cells) == len(sentence.cells) and sub_sentence.count == sentence.count:
                    self.knowledge.remove(sub_sentence)

                else:
                    # new_cells are equal to the longer sentence
                    new_cells = copy.deepcopy(sentence.cells)
                    new_count = sentence.count - sub_sentence.count
                    # remove each cell from the shorter sentence to generate brand new sentence
                    for cell in sub_sentence.cells:
                        new_cells.remove(cell)
                    # add the new sentence to the KB
                    one_more_sentence = Sentence(new_cells, new_count)
                    if one_more_sentence not in self.knowledge:
                        self.knowledge.append(one_more_sentence)

        if len(new_mines) != 0:
            return new_mines
        elif len(new_safes) != 0:
            return new_safes
        else:
            return None

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

        # 1)
        self.moves_made.add(cell)

        # 2)
        self.mark_safe(cell)

        # 3) take the cell height, width and create a sentence with all neighbouring cells
        # (which state is still undetermined) = count
        temp_sentence = set()
        temp_count = count
        # check all cells from height +1 to -1
        for row in (-1, 0, 1):
            # check all cells from width +1 to -1
            for column in (-1, 0, 1):
                temp_cell = ((cell[0] + row), (cell[1] + column))

                # check if it is the current cell
                if temp_cell[0] == cell[0] and temp_cell[1] == cell[1]:
                    continue

                # check if the row is out of the game field
                if temp_cell[0] > self.height - 1 or temp_cell[0] < 0:
                    continue

                # check if the column is out of the game field
                if temp_cell[1] > self.width - 1 or temp_cell[1] < 0:
                    continue

                # if cell's state is known to be safe -> ignor
                if temp_cell in self.safes:
                    continue

                # check if any of the surrounding cells are known to be mine
                if temp_cell in self.mines:
                    temp_count -= 1
                    continue

                # check if the cell is known to be safe
                if temp_cell in self.safes:
                    continue

                # add cell to the new sentence
                temp_sentence.add(temp_cell)

        # add sentence to the knowledge base
        new_sentence = Sentence(temp_sentence, temp_count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # infer new safes, new mines and new sentences as long as new knowledge can be generated
        while True:
            p = self.infer()
            if p is None:
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        for cell in self.safes:
            if cell in self.moves_made:
                continue
            else:
                self.moves_made.add(cell)
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        free_cells = []
        for i in range(self.width):
            for j in range(self.height):
                cell = (i, j)
                free_cells.append(cell)

        for each in copy.deepcopy(self.mines):
            if each in free_cells:
                free_cells.remove(each)
        for each in copy.deepcopy(self.moves_made):
            if each in free_cells:
                free_cells.remove(each)

        if len(free_cells) == 0:
            return None
        else:
            random_int = random.randint(0, len(free_cells) - 1)
            random_move = free_cells[random_int]
            return random_move
