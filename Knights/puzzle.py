import symbol

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
A_0_statement = And(AKnight, AKnave)
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    Biconditional(A_0_statement, AKnight)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
A_1_statement = And(BKnave, AKnave)
B_1_statement = Symbol("''")
knowledge1 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    Biconditional(A_1_statement, AKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
A_2_statement = Biconditional(AKnight, BKnight)
B_2_statement = Not(Biconditional(AKnight, BKnight))
knowledge2 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),

    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    Biconditional(A_2_statement, AKnight),
    Biconditional(B_2_statement, BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
A_3_statement = Or(AKnight, AKnave)
B_3_statement = And(Implication(A_3_statement, BKnave), CKnave)
C_3_statement = AKnight
knowledge3 = And(
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),

    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    Biconditional(A_3_statement, AKnight),
    Biconditional(B_3_statement, BKnight),
    Biconditional(C_3_statement, CKnight)
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