import kagglehub
import pandas as pd
import os
import re
def get_dataframe():
    path = kagglehub.dataset_download("essarabi/ultimate-us-election-dataset")
    print("Path to dataset files:", path)
    csv_file_path = os.path.join(path, "US_Election_dataset_v1.csv")
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
    else:
        print(f"Error: CSV file not found at {csv_file_path}")

    df = df.drop("Unnamed: 0", axis=1)

    percentages_as_strings = [
        'Population with less than 9th grade education',
        'Population with 9th to 12th grade education, no diploma',
        'High School graduate and equivalent',
        'Some College,No Degree',
        'Associates Degree',
        'Bachelors Degree',
        'Graduate or professional degree'
    ]

    df[percentages_as_strings] = df[percentages_as_strings].apply(lambda x: x.str.replace('%', '').astype('float64')/100)

    df.rename(columns={'Mean income (dollars)': 'x'}, inplace=True)
    df['Mean income (dollars)'] = df['x'].apply(lambda x: x.replace('$', '').replace(',', '')).astype(int)
    df.drop(columns=['x'], inplace=True)

    df.rename(columns={'Median income (dollars)': 'x'}, inplace=True)
    df['Median income (dollars)'] = df['x'].apply(
        lambda x: int(x.replace('$', '').replace(',', '')) if x.replace('$', '').replace(',', '').lstrip('-').isdigit() else None
    )
    df.drop(columns=['x'], inplace=True)

    out_of_scale_percentages = df.filter(regex='Percentage|percentage|%').columns

    df[out_of_scale_percentages] = df[out_of_scale_percentages].apply(lambda x: x / 100 if x.max() > 1 else x)
    df[out_of_scale_percentages].head()

    df["state"] = df["state"].apply(format_state_name)

    return df

def format_state_name(state_name):
    if state_name == "DistrictofColumbia":
        return "District of Columbia"

    return re.sub(r'([a-z])([A-Z])', r'\1 \2', state_name)

get_dataframe()