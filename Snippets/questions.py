import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, returns a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's content as a string.
    """

    os.chdir(directory)  # Change directory

    corpus = os.listdir()  # Create a list of all files in directory
    
    # Create a dictionary of .txt filenames and corresponding content strings
    files = dict()
    for i in corpus:
        files.setdefault(i)
        with open(i, "r", encoding='utf-8') as f:
            files[i] = f.read()
   
    return files


def tokenize(document):
    """
    Given a `document` (string), returns a list of all of the
    words in that document, in order.

    Converst all words to lowercase and removes any
    punctuation or English stopwords.
    """
 
    words = []  # Initialise list of words

    # Split up sentences into tokens
    tokens = nltk.word_tokenize(document)  

    for token in tokens:   
        token = token.lower()  # Make all lowercase
        if token in nltk.corpus.stopwords.words("english"):  # Remove English stopwords
            continue
        if token in string.punctuation:  # Remove punctuation
            continue
        
        words.append(token)  # Append token to list of words

    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps the names of .txt files 
    to lists of their words, returns a `idfs` dictionary that maps words to their 
    inverse document frequency (IDF) values.
    """
    
    idfs = dict()  # Initialise dictionary of words and corresponding IDFs
        
    for txt_file in documents:
        list_unique = []  # Create a list of unique words for each .txt file

        # Count the number of times each word appears in a .txt file
        for word in documents[txt_file]:
            if word not in list_unique:
                list_unique.append(word)
                idfs.setdefault(word, 0)
                idfs[word] +=1
    
    # Calculate IDF values for each word in `idfs` dictionary
    for word in idfs.keys():
        idfs[word] =  math.log(len(documents) / idfs[word])

    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping the names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), returns a list of the filenames of the the `n` top
    files that match the query, ranked according to term frequency-inverse document frequency (TF-IDF).
    """

    # Create a TF-IDF dictionary
    tf_idf = dict()
    
    for txt_file in files:
        tf_idf.setdefault(txt_file, 0)
        
        # Update TF-IDF value for each .txt file
        for word in query:
            if word in files[txt_file]:
                tf_idf[txt_file] += files[txt_file].count(word) * idfs[word] 

    # Sort dictionary by TF-IDF values in descending order
    tf_idf = dict(sorted(tf_idf.items(), key=lambda x: x[1], reverse=True))

    # Return a list of the top `n` .txt filenames maching the query
    top_n = list(tf_idf.keys())[:n]

    return top_n

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), returns a list of the `n` top sentences that match
    the query, ranked according to their SUMMED inverse inverse document frequency (IDF) 
    and then by their query term density (QTD). 
    """
    
    # Create a dictionary of all sentences and their IDF (summed) and QTD values (list[IDF, QTD])
    ranking = dict()  
    for sentence in sentences: 
        ranking.setdefault(sentence, [0, 0])
        for word in query:
            if word in sentences[sentence]: 
                ranking[sentence][0] += idfs[word]  # IDF
                ranking[sentence][1] += list(sentences[sentence]).count(word)/len(sentences[sentence]) # QTD

    # Sort dictionary values by IDF (descending) and then QTD (descending)
    ranking = dict(sorted(sorted(ranking.items(), key=lambda x: x[0], reverse=True), key=lambda x: x[1], reverse=True))

    # Return a list of the top `n` sentences maching the query
    top_n = list(ranking.keys())[:n]

    return top_n
    

if __name__ == "__main__":
    main()