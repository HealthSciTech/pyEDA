# Importing necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

def knnClassifier(X, Y, K=range(1,100)):
  """
  Args:
    X (arr): MxN array of M training examples with N features each.
    Y (arr): M, or M,1 array of target values associated with each data.
    K (arr): M, or M,1 array of different number of neighbors for tunning using validation data.
             By default is: range(1,100)

  Returns:
    learner: The best learner trained on the train data
    accuracy: Accuracy rate of the best learner on validation data
  """
  Xtr, Xva, Ytr, Yva = train_test_split(X,
                                        Y,
                                        test_size=.25)

  accuracy = 0
  for i,k in enumerate(K):
    neigh = KNeighborsClassifier(n_neighbors=k)
    newLearner = neigh.fit(Xtr, Ytr)
    YvaHat = newLearner.predict(Xva)
    newAccuracy = accuracy_score(Yva, YvaHat)
    if (newAccuracy >= accuracy):
      learner = newLearner
      accuracy = newAccuracy

  return learner, accuracy