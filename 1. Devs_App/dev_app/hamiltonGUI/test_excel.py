import pandas as pd

num_sample = 10
keys = ["A","B","C","D","E","F","G","H"]

template = pd.read_excel('LIMS_HBV_template.xlsx', engine='openpyxl',header=None)
output = template.copy()

row_index = 22
count = 0
        
# Loop through the number of samples and key values
for i in range(num_sample):
    for j, key in enumerate(keys):
        if i == 0 and j < 6:
            pass
        else:
            output.iloc[row_index,0] = f'{key}0{i+1}'
            output.iloc[row_index,1] = "FAM"
            output.iloc[row_index,2] = "HEX"
            output.iloc[row_index,7] = "Unknown"
            output.iloc[row_index,9] = "HBV"
            output.iloc[row_index,10] = "IC"
            output.iloc[row_index,8] = 1
            count+=1
            row_index+=1
            if count == num_sample:
                break
            
    if count == num_sample:
        break

template.to_excel('test.xlsx', index=False,header=False)


