import nltk
import sys


TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | S Conj S
NP -> N | AP N | Det N | Det AP N | NP PP 
VP -> V | V NP | V PP | V NP PP | VP Adv | Adv VP
PP -> P NP
AP -> Adj | Adj AP 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Converts `sentence` to a list of its words, 
    where all words are lowercase and 
    contain at least one alphabetic character.
    """
    
    words = []  # Initiate list of words

    # Split up sentences into tokens
    tokens = nltk.word_tokenize(sentence)  

    for token in tokens: 
        token = token.lower()  # Ensure lowercase

        for character in str(token): # Ensure at least one alphabetic character
            if character.isalpha():
                words.append(token)
                break

    return words

def np_chunk(tree):
    """
    Returns a list of all noun phrase chunks in the `sentence tree`.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    NP_chuncks = []  # Initiate list of noun phrase chunks
    
    # Get all subtrees of label 'NP'
    for subtree in tree.subtrees(lambda t: t.label() =='NP'):  
        
        # Get all lables of subtrees of subtree
        sub_subtree_labels = [] 
        for sub_subtree in subtree.subtrees():  
            sub_subtree_labels.append(sub_subtree.label())
        
        # Allow a single NP label per subtree
        if sub_subtree_labels.count('NP') == 1:  
            NP_chuncks.append(subtree)

    return NP_chuncks


if __name__ == "__main__":
    main()