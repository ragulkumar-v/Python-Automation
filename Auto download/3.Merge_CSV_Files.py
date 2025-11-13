import os
import pandas as pd

def merge_csv_files(input_folder, output_file):
    # List to hold dataframes
    dfs = []

    # Get a list of all CSV files in the input folder
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    # Check if there are any CSV files in the folder
    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    # Read the first file and store its data
    first_file_path = os.path.join(input_folder, csv_files[0])
    first_df = pd.read_csv(first_file_path)
    dfs.append(first_df)

    # Loop through the remaining files and append their data
    for csv_file in csv_files[1:]:
        file_path = os.path.join(input_folder, csv_file)
        df = pd.read_csv(file_path)
        dfs.append(df.iloc[1:])  # Skip the header row

    # Concatenate all dataframes
    merged_df = pd.concat(dfs, ignore_index=True)

    # Write the merged dataframe to the output file
    merged_df.to_csv(output_file, index=False)

    print(f"Merged CSV file saved to {output_file}")

# Example usage
input_folder = 'C:/RA work/SEC Rule 605 Datasets/EXBL/csv'  # Replace with your input folder path
output_file = 'C:/RA work/SEC Rule 605 Datasets/EXBL/EXBL.csv'  # Replace with your desired output file path

merge_csv_files(input_folder, output_file)