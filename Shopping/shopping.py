import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Loads shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Returns a tuple `(evidence, labels)`.
    """
    
    # Read data in from csv file
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        # Create list of data
        data = [] 

        # Month to integer transformation dictionary
        month_to_int ={"Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5, "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11}

        for row in reader:
            data.append({
                "evidence": [int(row[0]), # Administrative, an integer
                float(row[1]), # Administrative_Duration, a floating point number
                int(row[2]), # Informational, an integer
                float(row[3]), # Informational_Duration, a floating point number
                int(row[4]), # ProductRelated, an integer
                float(row[5]), # ProductRelated_Duration, a floating point number
                float(row[6]), # BounceRates, a floating point number
                float(row[7]), # ExitRates, a floating point number
                float(row[8]), # PageValues, a floating point number
                float(row[9]), # SpecialDay, a floating point number             
                int(month_to_int[row[10]]), # Month, an index from 0 (January) to 11 (December)
                int(row[11]), # OperatingSystems, an integer
                int(row[12]), # Browser, an integer
                int(row[13]), # Region, an integer
                int(row[14]), # TrafficType, an integer
                int(0) if row[15] == "New_Visitor" else int(1), # VisitorType, an integer 0 (not returning) or 1 (returning)
                int(0) if row[16] == "FALSE" else int(1)], # Weekend, an integer 0 (if false) or 1 (if true)
                "label": int(0) if row[17] == "FALSE" else int(1) # Purchase, an integer 0 (if false) or 1 (if true)
            })

    # Separate data into evidence and labels lists
    evidence = [row["evidence"] for row in data]
    labels = [row["label"] for row in data]

    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, returns a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors = 1)
    knn_model = model.fit(evidence, labels)

    return knn_model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    returns a tuple (sensitivity, specificty).
    """

    TP = 0 # True positives
    TN = 0 # True negatives
    FP = 0 # False positives
    FN = 0 # False negatives

    for i in range(len(labels)):
        if labels[i] == 1: 
            if labels[i] == predictions[i]:
                TP += 1
            if labels[i] != predictions[i]:
                FN += 1
        if labels[i] == 0: 
            if labels[i] == predictions[i]:
                TN += 1
            if labels[i] != predictions[i]:
                FP += 1

    sensitivity = TP/(TP+FN)
    specificity = TN/(TN+FP)

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()