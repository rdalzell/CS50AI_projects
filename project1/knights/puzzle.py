from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    And(Or(AKnave,AKnight), Not(And(AKnave,AKnight))),  # A must be either a Knave or Knight XOR
    Implication(AKnave,Not(And(AKnight,AKnave))), # If A is a knave -> inverse their statement because they are lying!
    Implication(AKnight,(And(AKnight,AKnave))) # If A is a knight -> Statement must be true
)
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnave,AKnight), Not(And(AKnave,AKnight))), # A must be either a Knave or Knight XOR
    And(Or(BKnave,BKnight), Not(And(BKnave,BKnight))), # B must be either a Knave or Knight XOR
    Implication(AKnave,Not(And(AKnave,BKnave))), # If A is a knave -> inverse their statement because they are lying!
    Implication(AKnight,(And(AKnave,BKnave)))    
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnave,AKnight), Not(And(AKnave,AKnight))),# A must be either a Knave or Knight XOR
    And(Or(BKnave,BKnight), Not(And(BKnave,BKnight))),# B must be either a Knave or Knight XOR
    Implication(AKnight, Or(And(AKnave,BKnave),And(AKnight,BKnight))),
    Implication(AKnave, Not(Or(And(AKnave,BKnave),And(AKnight,BKnight)))),
    Implication(BKnight, Or(And(AKnave,BKnight),And(AKnight,BKnave))),
    Implication(BKnave, Not(Or(And(AKnave,BKnight),And(AKnight,BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnave,AKnight), Not(And(AKnave,AKnight))), # XOR 
    And(Or(BKnave,BKnight), Not(And(BKnave,BKnight))), # XOR 
    And(Or(CKnave,CKnight), Not(And(CKnave,CKnight))), # XOR
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    Implication(BKnight, And(CKnave, Implication(AKnight, BKnight))),
    Implication(BKnave, Not(And(CKnave, Implication(AKnight, BKnight)))),
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]

    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")
                else:
                    print(f"")


if __name__ == "__main__":
    main()
