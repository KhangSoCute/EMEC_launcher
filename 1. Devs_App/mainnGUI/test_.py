import pandas as pd

# Load Excel file with header=None
df = pd.read_csv('LIMS_HBV_template.csv', header=None)

# Print the DataFrame
print(len((df.columns)))

empty_list = [""]*30
