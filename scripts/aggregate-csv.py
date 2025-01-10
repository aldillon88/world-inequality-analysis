import pandas as pd
import numpy as np
import os
import re
import time
import json

start_time = time.time()

# Define file paths.
script_dir = os.path.dirname(__file__)  
folder_path = os.path.abspath(os.path.join(script_dir, "../data"))  
processed_path = os.path.join(folder_path, "processed")
aggregate_path = os.path.join(folder_path, "aggregated")

# Define regex patterns for file names.
source_csv_pattern = "^[A-Z]{2}\.csv$"

# Define a schema.
expected_cols = [
	'country',
	'variable',
	'year',
	'value',
	'age',
	'pop',
    'countryname',
	'shortname',
	'shorttype',
	'shortpop',
	'shortage',
	'unit',
	'source',
	'method',
    'value_usd',
	'value_ppp',
	'region',
	'subregion',
    'value_usd_per_capita',
	'value_pct_national_income'
	]

col_check_set = set()
col_check_dict = {'failed_country' : []}

# Preload files
files = os.listdir(processed_path)
data_files = [file for file in files if re.match(pattern=source_csv_pattern, string=file)]
data_files.sort()

for i, file in enumerate(data_files):

	path = os.path.join(processed_path, file)
	df = pd.read_csv(path, keep_default_na=False, na_values=[''])
	col_check_set.add(len(df.columns))
		
	if set(df.columns) == set(expected_cols):
		for name, data in df.groupby('shortname'):
			if i == 0:
				data.to_csv(f"{aggregate_path}/{name}.csv", mode='a', header=True, index=False)
			else:
				data.to_csv(f"{aggregate_path}/{name}.csv", mode='a', header=False, index=False)
	
	else:
		if 'fail' not in col_check_dict.keys():
			col_check_dict['fail'] = 1
		else:
			col_check_dict['fail'] += 1
		col_check_dict['failed_country'].append(file[:2])
		print(df.columns)

end_time = time.time()
print(f"Execution time: {end_time - start_time:.4f} seconds")
print(col_check_set)
print(col_check_dict)