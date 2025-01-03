import pandas as pd
import numpy as np
import os
import re

# Define file paths.
script_dir = os.path.dirname(__file__)  
folder_path = os.path.abspath(os.path.join(script_dir, "../data"))  
unprocessed_path = os.path.join(folder_path, "unprocessed")
processed_path = os.path.join(folder_path, "processed")

# Define regex patterns for file names.
data_pattern = "^WID_data_[A-Z]{2}\.csv$"
meta_pattern = "^WID_metadata_[A-Z]{2}\.csv$"

# Define which columns to drop.
cols_to_drop = [
	'simpledes',
	'technicaldes',
	'extrapolation',
	'data_points',
	'age',
	'pop'
]

# Preload files
files = os.listdir(unprocessed_path)
data_files = [file for file in files if re.match(pattern=data_pattern, string=file)]
meta_files = {file[13:15]: file for file in files if re.match(pattern=meta_pattern, string=file)}

# Load the list of variables required for the analysis.
variables_to_analyze = pd.read_csv(f"{folder_path}/reference/variables_to_analyze.csv")
variables_for_conversion = pd.read_csv(f"{folder_path}/reference/vars_for_currency_conversion.csv")

for data_filename in data_files:

	# Isolate the country code for each file, eg. US.
	country_code = data_filename[9:11]

	if country_code in meta_files:

		data_path = os.path.join(unprocessed_path, data_filename)
		meta_path = os.path.join(unprocessed_path, meta_files[country_code])
		data_df = pd.read_csv(data_path, delimiter=';')
		meta_df = pd.read_csv(meta_path, delimiter=';', usecols=lambda col: col not in cols_to_drop)
		merged_df = pd.merge(left=data_df, right=meta_df, on=['country', 'variable'], suffixes=('', '_x'))

		# Filter by variables required for the analysis.
		filtered_df = merged_df[merged_df['variable'].isin(variables_to_analyze['variable'])].copy()

		if filtered_df.shape[0] > 0:

			# Create a mapping from 'year' to 'local_currency_per_usd' / 'ppp_conversion_factor_usd'
			ppp = filtered_df[filtered_df['variable'] == 'xlcuspi999'][['year', 'value']].copy()
			fx = filtered_df[filtered_df['variable'] == 'xlcusxi999'][['year', 'value']].copy()
			ppp_map = ppp.set_index('year')['value'].to_dict()
			fx_map = fx.set_index('year')['value'].to_dict()

			# Add columns for converted values - PPP and USD
			filtered_df.loc[:, 'value_usd'] = np.where(
				filtered_df['variable'].isin(variables_for_conversion['variable']),
				filtered_df['value'] / filtered_df['year'].map(fx_map),
				filtered_df['value']
			)

			filtered_df.loc[:, 'value_ppp'] = np.where(
				filtered_df['variable'].isin(variables_for_conversion['variable']),
				filtered_df['value'] / filtered_df['year'].map(fx_map),
				filtered_df['value']
			)

			filtered_df.to_csv(os.path.join(processed_path, f"{country_code}.csv"), index=False)


print('Task completed successfully.')
