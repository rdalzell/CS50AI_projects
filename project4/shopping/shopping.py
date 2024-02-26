import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB

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

    print ("PREDICTIONS!", predictions)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")



def convert_month(m):

    map = {
        'Jan' : 0,
        'Feb' : 1,
        'Mar' : 2,
        'Apr' : 3,
        'May' : 4,
        'June' : 5,
        'Jul' : 6,
        'Aug' : 7,
        'Sep' : 8,
        'Oct' : 9,
        'Nov' : 10,
        'Dec' : 11,
    }

    return map[m]


def convert_ints(d):
    keys = ['Administrative', 'Informational', 'ProductRelated', 'Month', 'OperatingSystems', 'Browser', 'Region','TrafficType']
    for k in keys:
        d[k] = int(d[k])
    return d

def convert_floats(d):
    keys = ['Administrative_Duration', 'Informational_Duration', 'ProductRelated_Duration', 'BounceRates','ExitRates', 'PageValues', 'SpecialDay']
    for k in keys:
        d[k] = float(d[k])
    return d

def convert_dict(d):

    d['Month'] = convert_month(d['Month'])
    d['VisitorType'] = 1 if d['VisitorType']=='Returning_Visitor' else 0
    d['Weekend'] = 1 if d['Weekend']=='TRUE' else 0
    d['Revenue'] = 1 if d['Revenue']=='TRUE' else 0

    d = convert_ints(d)
    d = convert_floats(d)
    return list(d.values())

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename, 'r') as read_obj: # read csv file as a list of lists
        reader = csv.DictReader(read_obj)
        a = list(reader) # Pass reader object to list() to get a list of lists

    list_of_rows = [convert_dict(x) for x in a]

    print(list_of_rows[0])
    print(list_of_rows[1])

    list_of_rows.pop(0)
    evidence = [x[:-1] for x in list_of_rows]
    labels = [x[-1] for x in list_of_rows]

    return (evidence, labels)

    


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    knn = KNeighborsClassifier(n_neighbors=1)
    #knn = svm.SVC()
    #knn = Perceptron()
    knn.fit(evidence, labels)

    return knn



def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    correct_p, correct_n = 0,0 
    pos_cnt, neg_cnt = 0,0

    for a, b in zip(labels, predictions):
        if a:
            pos_cnt +=1
            if a == b: 
                correct_p += 1

        if not a:
            neg_cnt += 1
            if a == b:
                correct_n += 1

    return (correct_p/pos_cnt, correct_n/neg_cnt)



if __name__ == "__main__":
    main()
