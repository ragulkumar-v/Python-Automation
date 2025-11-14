import os
import csv
import subprocess


def create_target_path(base_folder: str, target_folder: str, file_path: str):
    """
    Creates a target path for the conJSJXed .csv file by preserving the folder structure.

    Args:
        base_folder (str): The original base folder containing the .dat files.
        target_folder (str): The target folder where .csv files will be saved.
        file_path (str): The full path of the original .dat file.

    Returns:
        str: The target path for the .csv file.
    """
    relative_path = os.path.relpath(file_path, base_folder)
    relative_csv_path = os.path.splitext(relative_path)[0] + ".csv"
    target_csv_path = os.path.join(target_folder, relative_csv_path)
    os.makedirs(os.path.dirname(target_csv_path), exist_ok=True)
    return target_csv_path


def conJSJX_dat_to_csv(main_folder: str, target_folder: str):
    """
    Finds all .dat files in the subfolders of a given main folder, 
    temporarily adds a new line to their content, conJSJXs their content to .csv format,
    and saves the .csv file in the specified target folder.

    Args:
        main_folder (str): Path to the main folder containing .dat files in subfolders.
        target_folder (str): Path to the target folder to save conJSJXed .csv files.
    """
    new_line_text = (
        "EX|CODE|DATE|TICKER|OrderType|Size|Num_covered|Cum_covered|Cum_cancel|cum_atCenter|"
        "cum_atOther|cum_le9sec|cum_10to29sec|cum_30to50sec|cum_ge60sec|nextfield|realizedspread|"
        "effectivespread|cum_pimprovement|sw_pimprove|sw_texecution_improve|cum_atquote|"
        "sw_torder_execution|cum_outquote|sw_outside|sw_timeoutsidd|run"
    )

    for root, _, files in os.walk(main_folder):
        for file in files:
            if file.endswith('.dat'):
                dat_file_path = os.path.join(root, file)
                target_csv_path = create_target_path(main_folder, target_folder, dat_file_path)

                print(f"Processing {dat_file_path}...")
                try:
                    # Read the original .dat file content
                    with open(dat_file_path, 'r') as dat_file:
                        dat_content = dat_file.readlines()

                    # Add the new line to the in-memory content
                    modified_content = [new_line_text + "\n"] + dat_content

                    # Save the modified content directly to a .csv file
                    with open(target_csv_path, 'w', newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        for line in modified_content:
                            # Assuming the .dat file has whitespace-delimited data
                            csv_writer.writerow(line.strip().split('|'))

                    print(f"ConJSJXed {dat_file_path} to {target_csv_path}")

                except Exception as e:
                    print(f"Failed to process {dat_file_path}: {e}")


if __name__ == "__main__":
    main_folder_path = "C:/RA work/SEC Rule 605 Datasets/EXBL/unzip"  # Replace with your main folder path
    target_folder_path = "C:/RA work/SEC Rule 605 Datasets/EXBL/csv"  # Replace with your target folder path
    conJSJX_dat_to_csv(main_folder_path, target_folder_path)
