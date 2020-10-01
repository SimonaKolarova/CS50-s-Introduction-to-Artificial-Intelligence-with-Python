from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

def knight(Sentence):
    return Sentence

def knave(Sentence):
    return Not(Sentence)

# Puzzle 0

# A says "I am both a knight and a knave."
sentence0A = And(AKnight, AKnave)

knowledge0 = And(
    # A is a knight or a knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    
    # Consider both options for A
    Or(
        # A is a knight
        And(AKnight, knight(sentence0A)), 
        # A is a knave
        And(AKnave, knave(sentence0A))
    )
)

# Puzzle 1

# A says "We are both knaves."
sentence1A = And(AKnave, BKnave)
# B says nothing.

knowledge1 = And(
    # A is a knight or a knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is a knight or a knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    
    # Consider both options for A
    Or(
        # A is a knight
        And(AKnight, knight(sentence1A)), 
        # A is a knave
        And(AKnave, knave(sentence1A))
    )
)

# Puzzle 2

# A says "We are the same kind."
sentence2A = Or(And(AKnight, BKnight), And(AKnave, BKnave))
# B says "We are of different kinds."
sentence2B = Or(And(AKnight, BKnave), And(AKnave, BKnight))

knowledge2 = And(
    # A is a knight or a knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is a knight or a knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    
    # Consider both options for A
    Or(
        # A is a knight
        And(AKnight, knight(sentence2A)), 
        # A is a knave
        And(AKnave, knave(sentence2A))
    ),
    # Consider both options for B
    Or(
        # B is a knight
        And(BKnight, knight(sentence2B)), 
        # B is a knave
        And(BKnave, knave(sentence2B))
    )
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
sentence3A0 = AKnight
sentence3A1 = AKnave
sentence3A = And(Or(sentence3A0, sentence3A1), Not(And(sentence3A0, sentence3A1)))
# B says "A said 'I am a knave'."
sentence3B0 = sentence3A1
# B says "C is a knave."
sentence3B1 = CKnave
# C says "A is a knight."
sentence3C = AKnight

knowledge3 = And(
    # A is a knight or a knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # B is a knight or a knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    # C is a knight or a knave but not both
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # Consider both options for A
    Or(
        # A is a knight
        And(AKnight, knight(sentence3A)), 
        # A is a knave
        And(AKnave, knave(sentence3A))
    ),
    # Consider both options for B
    Or(
        # B is a knight
        And(BKnight, knight(sentence3B0), knight(sentence3B1)), 
        # B is a knave
        And(BKnave, knave(sentence3B0), knave(sentence3B1))
    ),
    # Consider both options for C
    Or(
        # C is a knight
        And(CKnight, knight(sentence3C)), 
        # C is a knave
        And(CKnave, knave(sentence3C))
    )
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


if __name__ == "__main__":
    main()
