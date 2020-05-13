# Importing necessary libraries
import csv

def openShimmerFile(url, column_name):
  '''finding to open the files
    Funcion that extracts gsr data from the files
    
    Parameters
    ----------
    url : String
        The address of the csv file from Shimmer
	column_name : String
        The name of the column to extract its data from the file
    
    Returns
    -------
    req_data : 1-d array
        Array containing the gsr data
  '''

  req_data = []
  index = -1

  # Read File
  with open(url) as f:
    if ('csv' in url):
      reader = csv.reader(f, delimiter=',')
    else:
      reader = csv.reader(f, delimiter='\t')
    # Store data in lists
    sep = reader.__next__()
    sep = reader.__next__()
    sep = reader.__next__()		
    forth_row = reader.__next__()
    shimmer_header = []
    data_header = []
    calib_header = []
    for i,column in enumerate(forth_row):
      if (column == column_name):
        index = i
    reader.__next__()

    if (index < 0):
      print("Column not found!")
        
    for row in reader:
      if (index <= len(row)):
        req_data.append(float(row[index]))

  return req_data