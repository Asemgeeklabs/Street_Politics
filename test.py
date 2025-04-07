import shutil
import os

def remove_folder(folder_path):
    """
    Remove the entire folder and its contents.

    :param folder_path: Path to the folder to be removed
    """
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' has been removed.")
    else:
        print(f"Folder '{folder_path}' does not exist.")

remove_folder("downloads/ff")

