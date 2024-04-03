'''
This function's purpose is to bin the lengths and average protein expression data collected from fingernail
analyses. The script assumes that the input will be a csv file, and that the x-values (standardized arc lenghts)
and y-values (ratio of expression cortex/cytoplasm) will be labeled in columns as x1, y1, x2, y2, etc. Any
cells with "0.0" or a division error after standard length 1.0 will need to be removed, as the extra 0s and
divison errors will break the function even though .dropna accounts for unpaired values.
'''

import pandas as pd
import numpy as np
import os


# Import libraries for data handling

def process_data(file_path, output_file):
    # Read in the data
    data = pd.read_csv(file_path)

    all_averages = []  # A list to store all the averages in for export

    time_pts = int(len(data.columns) / 2)
    # Division by 2 assumes there are an even number of columns, which for this protocol,there should be.
    # time_pts is assigned an integer which should be equal to the number of time points included in the data set

    # Iterate over the data in each time point
    for i in range(1, time_pts + 1):
        x_col = f'x{i}'
        y_col = f'y{i}'

        # Drop rows where either x or y is not a number (NaN), including if it is blank. This can happen if the
        # line shifts during measurement and so is essential for integrity
        subset = data[[x_col, y_col]].dropna()

        # Bin the data by tenths; 10 bins from 0 to 1
        bins = np.linspace(0, 1, 11)
        bin_labels = np.arange(1, 11)  # Labels from 1 to 10

        subset['bin'] = pd.cut(subset[x_col], bins, labels=bin_labels, include_lowest=True)

        # Group by bin and calculate the mean of y-values
        averages = subset.groupby('bin')[y_col].mean().rename(f'Average_{i}').reset_index()

        # Print the current set to check function
        print(f"Averages for Set {i}:")
        print(averages)
        print()

        # Add dataframe to the list
        all_averages.append(averages.set_index('bin'))

    # Concat all averages to one dataframe for export
    final_df = pd.concat(all_averages, axis=1)

    # Save to CSV
    final_df.to_csv(output_file)

    # Print to check the output file was saved
    print(f"Data processed and saved to: {output_file}")


# Call the function and save the results. # Replace 'YourOutputFolder' with your folder name and 'all_sets_avgs'
# with the name you want the file saved under. Add to the path as needed.
file_path = '/Users/willburks/Desktop/data/Book1.csv.csv'  # Replace with the file path
output_file = os.path.join(os.path.expanduser('~'), 'Desktop', 'data', 'all_sets_avgs.csv')
process_data(file_path, output_file)
