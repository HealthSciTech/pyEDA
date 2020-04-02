import numpy as np

def TournamentSelection(Accuracy, Predict):
  """
  Args:
    Accuracy (dictionary): Dictionary mapping classifiers to their accuracy on the test data.
    Predict (dictionary): Dictionary mapping classifiers to their prediction array on the test data.

  Returns:
    finalPredict (array): M, or M,1 array of predictions on the test data.
  """
  sum = np.zeros(Predict['size'])
  count = 0
  for key in Accuracy:
    sum = sum+Accuracy[key]*Predict[key]
    count = count+1
	
  finalPredict = np.round(sum/count, 0)
  
  return finalPredict