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

    percentage_columns = [
        'Population with less than 9th grade education',
        'Population with 9th to 12th grade education, no diploma',
        'High School graduate and equivalent',
        'Some College,No Degree',
        'Associates Degree',
        'Bachelors Degree',
        'Graduate or professional degree'
    ]

    for col in percentage_columns:
        df[col] = df[col].astype(str).str.rstrip("%").astype("float64") / 100

    for col in ["Mean income (dollars)", "Median income (dollars)"]:
        df[col] = df[col].astype(str).str.replace(",", "", regex=False)
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    
    df["state"] = df["state"].apply(format_state_name)

    return df

def format_state_name(state_name):
    if state_name == "DistrictofColumbia":
        return "District of Columbia"

    return re.sub(r'([a-z])([A-Z])', r'\1 \2', state_name)

get_dataframe()