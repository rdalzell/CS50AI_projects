import sys

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
        print (self.domains, len(self.domains))

        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for v in self.domains:
            new_set = set()
            for word in self.domains[v]:
                if len(word) == v.length:
                    new_set.add(word)
            self.domains[v] = new_set         
            

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revise = False

        for v in self.crossword.overlaps:
            (a,b) = v
            if a == x and b == y:
                overlap = self.crossword.overlaps[v]
                if overlap: # I.e. there is a arc
                    print ("OVERLAP VARS", x, y, self.domains[x], self.domains[y])
                    (p1, p2) = overlap                    
                    print ("OVERLAP", p1, p2)

                    # Remove words from x domain that aren't consistent
                    new_set = set()
                    for word1 in self.domains[x]:
                        for word2 in self.domains[y]:
                            if word1[p1] == word2[p2]:
                                new_set.add(word1)

                    if new_set != self.domains[x]:
                        revise = True
                        print ("NEW SET", new_set)
                        self.domains[x] = new_set

        return revise 


 

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            arcs = []
            for i in self.crossword.overlaps:
                if self.crossword.overlaps[i]:
                    arcs.append(i)

        print ("INITIAL ARCS", arcs)
        while len(arcs) > 0:
            (x,y) = arcs[0]
            del arcs[0]
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for n in self.crossword.neighbors(x):
                    if n != y:
                        arcs.append((n,x))

        return True



    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        print ("assignment_complete", assignment)
        for v in self.domains:
            if v not in assignment:
                return False
            
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        print ("consistent", assignment)
        for variable1 in assignment:
            word1 = assignment[variable1]
            if variable1.length != len(word1):
                # word length doesn't satisfy constraints
                return False

            for variable2 in assignment:
                word2 = assignment[variable2]
                if variable1 != variable2:
                    if word1 == word2:
                        # two variables mapped to the same word
                        return False

                    overlap = self.crossword.overlaps[variable1, variable2]
                    if overlap is not None:
                        a, b = overlap
                        if word1[a] != word2[b]:
                            # words don't satisfy overlap constraints
                            return False

        return True
 


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        for v in self.domains:
            if v not in assignment:
                return v

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        print ("**** BACK TRACK *****")
        print (self.domains, len(self.domains))

        if self.assignment_complete(assignment):
            print ("Return Complete Assignment")
            return assignment
        
        var = self.select_unassigned_variable(assignment)

        for word in self.domains[var]:
            try_assign = { var : word}
            if self.consistent(try_assign):
                assignment[var] = word
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]

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
