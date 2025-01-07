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
	'pop',
	'longtype',
	'longpop',
	'longage'
]

# Preload files
files = os.listdir(unprocessed_path)
data_files = [file for file in files if re.match(pattern=data_pattern, string=file)]
meta_files = {file[13:15]: file for file in files if re.match(pattern=meta_pattern, string=file)}

# Load the list of variables required for the analysis.
variables_to_analyze = pd.read_csv(f"{folder_path}/reference/variables_to_analyze.csv")
variables_for_conversion = pd.read_csv(f"{folder_path}/reference/vars_for_currency_conversion.csv")

# Load region data for each country.
region_data = pd.read_csv(f"{folder_path}/reference/WID_countries.csv", delimiter=';', index_col='alpha2')[['region', 'region2']]
region_map = region_data['region'].to_dict()
subregion_map = region_data['region2'].to_dict()

with open(f"{folder_path}/reference/public_spending_vars.json", 'r') as file:
    public_spending_vars = json.load(file)

public_spending_total = public_spending_vars['Total']
public_spending_per_capita = public_spending_vars['Average']
public_spending_pct_of_income = public_spending_vars['Wealth-income ratio']
ps_pc_pct_combined = public_spending_per_capita + public_spending_pct_of_income

total_rows = 0

step1 = 0
step2 = 0
step3 = 0

for data_filename in data_files:
	step1 += 1
	# Isolate the country code for each file, eg. US.
	country_code = data_filename[9:11]

	if country_code in meta_files:# and country_code == 'AD':
		step2 += 1

		data_path = os.path.join(unprocessed_path, data_filename)
		meta_path = os.path.join(unprocessed_path, meta_files[country_code])
		data_df = pd.read_csv(data_path, delimiter=';')
		meta_df = pd.read_csv(meta_path, delimiter=';', usecols=lambda col: col not in cols_to_drop)
		merged_df = pd.merge(left=data_df, right=meta_df, on=['country', 'variable'], suffixes=('', '_x'))

		# Filter by variables required for the analysis.
		filtered_df = merged_df[merged_df['variable'].isin(variables_to_analyze['variable'])].copy()

		# Add region data.
		

		if filtered_df.shape[0] > 0:
			step3 += 1

			# Create a mapping from 'year' to 'local_currency_per_usd' / 'ppp_conversion_factor_usd'
			ppp = filtered_df[filtered_df['variable'] == 'xlcuspi999'][['year', 'value']].copy()
			ppp_map = ppp.set_index('year')['value'].to_dict()
			fx = filtered_df[filtered_df['variable'] == 'xlcusxi999'][['year', 'value']].copy()
			fx_map = fx.set_index('year')['value'].to_dict()

			# Add columns for converted values - PPP and USD
			filtered_df.loc[:, 'value_usd'] = np.where(
				filtered_df['variable'].isin(variables_for_conversion['variable']),
				filtered_df['value'] / filtered_df['year'].map(fx_map),
				None
			)

			filtered_df.loc[:, 'value_ppp'] = np.where(
				filtered_df['variable'].isin(variables_for_conversion['variable']),
				filtered_df['value'] / filtered_df['year'].map(ppp_map),
				None
			)

			filtered_df['region'] = filtered_df['country'].map(region_map)
			filtered_df['subregion'] = filtered_df['country'].map(subregion_map)

			# Create a mapping to add per capita values to the rows containing totals (in currency only).
			per_capita = filtered_df[filtered_df['variable'].isin(public_spending_per_capita)][['year', 'shortname', 'shortage', 'value_usd']]
			per_capita_map = per_capita.set_index(['year', 'shortname', 'shortage'])['value_usd'].to_dict()

			filtered_df['key'] = list(zip(filtered_df['year'], filtered_df['shortname'], filtered_df['shortage']))
			filtered_df['value_usd_per_capita'] = filtered_df['key'].map(per_capita_map).where(
				filtered_df['variable'].isin(public_spending_total)
			)

			filtered_df_trimmed = filtered_df[~filtered_df['variable'].isin(ps_pc_pct_combined)].drop(columns=['key'])
			
			filtered_df_trimmed.to_csv(os.path.join(processed_path, f"{country_code}.csv"), index=False)

			total_rows += filtered_df_trimmed.shape[0]

end_time = time.time()

print(f"Execution time: {end_time - start_time:.4f} seconds")
print(f"Total number of rows processed: {total_rows}")
print(f"No. of countries left after step 1: {step1}")
print(f"No. of countries left after step 2: {step2}")
print(f"No. of countries left after step 3: {step3}")
print('Task completed successfully.')