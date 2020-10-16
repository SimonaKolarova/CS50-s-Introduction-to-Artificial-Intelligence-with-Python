import sys
import copy

from crossword import *
from operator import itemgetter

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Updates `self.domains` such that each variable is node-consistent.
        (Removes any values that are inconsistent with a variable's unary
        constraints, i.e., the length of the word.)
        """
        for space in self.domains:
            for word in list(self.domains[space]):
                if space.length != len(str(word)):
                    self.domains[space].remove(word)

    def revise(self, x, y):
        """
        Makes variable `x` arc consistent with variable `y`, 
        i.e., removes values from `self.domains[x]` for which there are no
        possible corresponding value for `y` in `self.domains[y]`.

        Returns True if a revision was made to the domain of `x`; 
        returns False if no revision was made.
        """

        revised = False # Initiate return boolean value 

        # Check for overlap between x and y 
        for var in self.crossword.overlaps:
            if var[0] == x and var[1] == y and self.crossword.overlaps[var] != None:
                overlap_position = self.crossword.overlaps[var]
                
                # Compare overlap letters for x and y 
                for word_x in list(self.domains[x]):
                    overlap_posibility = False # Initiate overlap posibility boolean 
                    for word_y in list(self.domains[y]):
                        
                        # If overlap between word_x and any word_y is possible
                        if str(word_x)[overlap_position[0]] == str(word_y)[overlap_position[1]]:
                            overlap_posibility = True
                            break

                    # If overlap between word_x and any word_y is not possible remove word_x
                    if overlap_posibility == False:
                        self.domains[x].remove(word_x)
                        revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Updates `self.domains` such that each variable is arc consistent.

        Returns True if arc consistency is enforced and no domains are empty;
        returns False if one or more domains end up empty.
        """

        # Create a list of all arcs in the problem if no list was passed to the function
        if arcs == None:
            arcs = []
            for var in self.crossword.overlaps:
                if self.crossword.overlaps[var] != None:
                    arcs.append(var)

        # Recursively enforce arc consistency
        while arcs:

            # Dequeue an arc to revise variable `x` against `y`
            x = arcs[0][0]
            y = arcs[0][1]
            arcs = arcs[1:]
            
            # If variable `x` was revised 
            if self.revise(x,y) == True:

                # If no possible `x` values left
                if self.domains[x] == None:
                    return False

                # Enqueue arcs dependent on `x` for revision
                for var in self.crossword.overlaps:
                    if var[1] == x and var[0] != y:
                        arcs.append(var)
                        
        return True

    def assignment_complete(self, assignment):
        """
        Detemermines whether `assignment` is complete
        (i.e., a single value is assigned to each crossword variable).
        Returns True if `assignment` is complete;
        returns False otherwise.
        """

        # Check if each variable has been assigned a value
        if len(assignment) != len(self.domains):
            return False   

        # Check if each variable has been assigned a single value 
        for var in assignment:
            if assignment[var] == None:
                return False

        return True

    def consistent(self, assignment):
        """
        Determines whether an `assignment` is consistent 
        (i.e., all words fit in crossword puzzle spaces, there are no conflicting characters
        and each assigned value is unique). 
        Returns True if `assignment` is consistent; return False otherwise.
        """
 
        for var in assignment:
            if assignment[var] != None: # Check consistency of assigned variables only
           
                # Check node consistency 
                for var1 in self.domains:
                    if var == var1 and var.length != var1.length:
                        return False

                # Check arc consistency of all variables overlaping `var`
                for overlap in self.crossword.overlaps:
                    if self.crossword.overlaps[overlap] != None and (overlap[0] == var or overlap[1] == var):
                        word_x = assignment[overlap[0]]
                        word_y = assignment[overlap[1]]
                        overlap_position = self.crossword.overlaps[overlap]

                        if word_x != None and word_y !=None:
                            if str(word_x)[overlap_position[0]] != str(word_y)[overlap_position[1]]:
                                return False

                # Check for non-distinct values accross asignment (i.e., values assigned to more than one variable)
                for var2 in assignment:
                    if var != var2 and assignment[var] == assignment[var2]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Returns a list of values in the domain of `var`, 
        in assending order by the number of values 
        they rule out for neighboring variables in `assignment`.
        """

        # Create a dictionary of words and corresponding number of eliminated neighbouring variables
        eliminations = {}

        for word in self.domains[var]:
            eliminations.setdefault(word, 0)

            # Check arc consistency
            for overlap in self.crossword.overlaps:
                if self.crossword.overlaps[overlap] != None:
                    overlap_position = self.crossword.overlaps[overlap]
                    
                    # If the variable of interest overalaps an assigned variable
                    if overlap[0] == var and assignment[overlap[1]] != None: 
                        word_x = assignment[overlap[1]]
                        if str(word)[overlap_position[0]] != str(word_x)[overlap_position[1]]:
                            eliminations[word] += 1       
        
        # Sort the dictionary by value in assending order
        eliminations = dict(sorted(eliminations.items(), key=lambda x:x[1]))

        return eliminations.keys()

    def select_unassigned_variable(self, assignment):
        """
        Returns an unassigned variable (i.e., not in `assignment`).
        Chooses the variable with the minimum number of remaining values
        in its domain. If there is a tie, chooses the variable with the highest
        degree. If there is a tie, any of the tied variables is selected.
        """
    
        # Create a list of tuples containing the the unassigned variables,
        # the corresponding number of values and corresponding number of neighbours
        unassigned_variables = []
        
        for var in self.domains:
            if assignment[var] == None:
                unassigned_variables.append((var, len(self.domains[var]), len(self.crossword.neighbors(var))))
                     
        # Sort by number of values in assending order and by neighbours in descending order
        unassigned_variables = sorted(sorted(unassigned_variables, key=itemgetter(2), reverse=True), key = itemgetter(1))
        
        return unassigned_variables[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, takes as input a partial `assignment` for the
        crossword and returns a complete `assignment` if possible to do so.
        If no assignment is possible, returns None.
        """

        # Create assignment if it does not exist
        if not assignment:
            for var in self.domains:
                assignment[var] = None
        
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment
        
        # Select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # Itterate over values for unassigned variable
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word 
            
            if self.consistent(assignment): # If assigned values is consistent with assignment
                
                # Recursively repeat the backtracking search 
                result = self.backtrack(assignment)
                if result != None:
                    return result

            assignment[var] = None # If assigned values is not consistent with assignment

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
