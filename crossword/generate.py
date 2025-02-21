import sys
import os
os.system('clear')
from crossword import *


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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # raise NotImplementedError
        for variable, domain in self.domains.items():
            word_length = variable.length
            for value in set(domain):
                if len(value) != word_length:
                    self.domains[variable].remove(value)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # raise NotImplementedError
        (i,j) = self.crossword.overlaps[x, y]
        revised = False
        for value_x in set(self.domains[x]):
            found = False
            character = value_x[i]
            for value_y in self.domains[y]:
                if value_y[j] == character:
                    found = True
                    continue
            if found == False:
                self.domains[x].remove(value_x)
                revised = True
        return revised
                    
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # raise NotImplementedError
        if arcs is None:
            arcs = [(x, y) for x in self.domains for y in self.crossword.neighbors(x)]
        
        while arcs:
            (x, y) = arcs.pop(0)
            revised = self.revise(x, y)

            if not self.domains[x]:
                return False
            
            if revised:
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z, x))
        return True
    
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # raise NotImplementedError
        for variable in self.domains:
            if variable in assignment:
                continue
            else: return False
        return True
            
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # raise NotImplementedError
        words = set()
        for variable, word in assignment.items():
            if word in words:
                return False
            else: words.add(word)

            if len(word) != variable.length:
                return False
            
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    [i, j] = self.crossword.overlaps[variable, neighbor]
                    character = word[i]
                    neighbor_word = assignment[neighbor]
                    if neighbor_word[j] != character:
                        return False
        return True
            
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # raise NotImplementedError
        neighbors = self.crossword.neighbors(var)
        unassigned_neighbors = set()
        for neighbor in neighbors:
            if neighbor in assignment:
                continue
            else: unassigned_neighbors.add(neighbor)

        least_constraint_dict = {}
        for word in self.domains[var]:
            count = 0
            for neighbor in unassigned_neighbors:
                (i,j) = self.crossword.overlaps[var, neighbor]
                character = word[i]
                values_neighbor = self.domains[neighbor]
                for value_neighbor in values_neighbor:
                    if character != value_neighbor[j]:
                        count += 1
            least_constraint_dict[word] = count
        return sorted(least_constraint_dict, key=lambda word: least_constraint_dict[word])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # raise NotImplementedError
        unassigned_variables = set()
        for variable in self.domains:
            if variable in assignment:
                continue
            else: unassigned_variables.add(variable)
        unassigned_variables_dict = {}
        for variable in unassigned_variables:
            num_remaining_values = len(self.domains[variable])
            num_neighbors = len(self.crossword.neighbors(variable))
            unassigned_variables_dict[variable] = {
                "num_remaining_values": num_remaining_values,
                "num_neighbors": num_neighbors
            }

        unassigned_variables_dict = sorted(
            unassigned_variables_dict.items(), 
            key=lambda item: (item[1]["num_remaining_values"], -item[1]["num_neighbors"])
            )
        
        first_variable = next(iter(unassigned_variables_dict))[0]
        return first_variable
    
    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # raise NotImplementedError
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        values = self.order_domain_values(var, assignment)
        for value in values:
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            else:
                assignment.pop(var)
        return None
                            
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        # sys.exit("Usage: python generate.py structure words [output]")
        structure = "data/structure1.txt"
        words = "data/words1.txt"
        output = "output1.png"
    else:    
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
