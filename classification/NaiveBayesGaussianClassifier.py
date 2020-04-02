# Importing necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

def NaiveBayesGaussianClassifier(X, Y):
  """
  Args:
    X (arr): MxN array of M training examples with N features each.
    Y (arr): M, or M,1 array of target values associated with each data.

  Returns:
    learner: The learner trained on the train data
    accuracy: Accuracy rate of the learner on validation data
  """
  Xtr, Xva, Ytr, Yva = train_test_split(X,
                                        Y,
                                        test_size=.25)

  learner = GaussianNB()
  learner.fit(Xtr, Ytr)

  # generate predictions
  YvaHat = learner.predict(Xva)

  # calculate accuracy
  accuracy = accuracy_score(Yva, YvaHat)

  return learner, accuracy