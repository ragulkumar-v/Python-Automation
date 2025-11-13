import os
import zipfile


def unzip_files_in_subfolders(main_folder: str, output_folder: str = None):
    """
    Unzips all .zip files inside the subfolders of a given main folder.

    Args:
        main_folder (str): Path to the main folder containing subfolders with .zip files.
        output_folder (str): Path to extract files. If None, extracts in the same folder as the .zip file.
    """
    if output_folder:
        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(main_folder):
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.normpath(os.path.join(root, file))
                extract_to = os.path.normpath(
                    output_folder if output_folder else root)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        print(f"Extracting {zip_path} to {extract_to}")
                        zip_ref.extractall(extract_to)
                except zipfile.BadZipFile:
                    print(f"Failed to unzip: {zip_path} (Bad zip file)")
                except Exception as e:
                    print(f"Error while unzipping {zip_path}: {e}")


# Example usage
if __name__ == "__main__":
    # Replace with your main folder path
    main_folder_path = os.path.normpath(
        "C:/RA work/SEC Rule 606 Datasets/Muriel Siebert/zip")
    output_folder_path = os.path.normpath(
        # Optional: Replace or set to None
        "C:/RA work/SEC Rule 606 Datasets/Muriel Siebert/unzip")
    unzip_files_in_subfolders(main_folder_path, output_folder_path)
