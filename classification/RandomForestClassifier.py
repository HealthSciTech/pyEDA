# Importing necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier as RandomForest

def RandomForestClassifier(X, Y, D=range(1,25)):
  """
  Args:
    X (arr): MxN array of M training examples with N features each.
    Y (arr): M, or M,1 array of target values associated with each data.
    D (arr): M, or M,1 array of different number for depths for tunning using validation data.
             By default is: range(1,100)

  Returns:
    learner: The learner trained on the train data
    accuracy: Accuracy rate of the learner on validation data
  """
  Xtr, Xva, Ytr, Yva = train_test_split(X,
                                        Y,
                                        test_size=.25)

  accuracy = 0
  for i,d in enumerate(D):
    newLearner = RandomForest(max_depth=d, random_state=42)
    newLearner.fit(Xtr, Ytr)
    YvaHat = newLearner.predict(Xva)
    newAccuracy = accuracy_score(Yva, YvaHat)
    if (newAccuracy >= accuracy):
      learner = newLearner
      accuracy = newAccuracy

  return learner, accuracy