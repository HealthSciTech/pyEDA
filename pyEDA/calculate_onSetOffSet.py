'''
Calculate the list of onSets and offSets based on phasic component of signal.
'''
def calculate_onSetOffSet(filtered_phasic_gsr, sample_rate, minDiff=0.5, onSetThreshold=0.01):
  # Some initializations
  onSet_offSet = []
  tmpSet = []
  onIsSet = False

  for i, data in enumerate(filtered_phasic_gsr):
    if (onIsSet):
      if (data < 0):
        tmpSet.append(i)
        timeDifference = tmpSet[1]-tmpSet[0]
        timeDifference = timeDifference/sample_rate
        if (timeDifference > minDiff):
          onSet_offSet.append(tmpSet)
        tmpSet = []
        onIsSet = False
    elif data > onSetThreshold:
      tmpSet.append(i)
      onIsSet = True

  return np.array(onSet_offSet)