def openShimmerFile(url, column_name):
    """
      url: The address of the csv file from Shimmer
      column_name: The name of the column to extract its data
      Example for Skin Conductance:
      url: default_exp_Session1_Shimmer_9301_Calibrated_PC.csv
      column_name: Shimmer_9301_GSR_Skin_Conductance_CAL
    """

    req_data = []
    index = -1

    # Read File
    with open(url) as f:
        reader = csv.reader(f, delimiter='\t')
        # Store data in lists
        sep = reader.__next__()
        second_row = reader.__next__()
        shimmer_header = []
        data_header = []
        calib_header = []
        for i,column in enumerate(second_row):
            if (column == column_name):
              index = i
        reader.__next__()

        if (index < 0):
            print("Column not found!")
        
        for row in reader:
            if (index <= len(row)):
                req_data.append(float(row[index]))

    return req_data