import os
import shutil
import pandas as pd


def move_file(file_name: str, folder_name: str):
    """Moves file to a folder

    Warning
    -------
    Implementing this function will override a file with the same name in the destination directory.

    Parameters
    ---------
    file_name:str
        The file you wish to move.
    folder_name: str
        The folder you wish to move your file to

    Returns
    -----
    None

    """
    file_path = file_name
    new_directory = folder_name
    # create a new directory
    os.makedirs(new_directory, exist_ok=True)
    # path of the file when moved
    destination_file = os.path.join(new_directory, os.path.basename(file_path))
    try:
        # move the file
        shutil.move(file_path, new_directory)
    except shutil.Error:
        """This error typically occurs when there is already a file with the same name in the 
            destination directory. If this is the case, we fill delete the original file"""
        os.remove(destination_file)
        # move the file
        shutil.move(file_path, new_directory)
    except FileNotFoundError:
        print(f"Please put the raw data file in the same directory as this python script. "
              f"If you think you have provided the file, please check if the file name is correct.")


def get_data_from(file_name: str, name_of_data_folder="raw_data"):
    """A function to read csv file and place it in a raw_data folder if the file is not already
    in it

    Parameters
    ----------
    file_name: str
        The name of the file you wish to read.

    name_of_data_folder: str
        The name of the folder containing data files. Default to raw_data


    Returns
    -------
    data: pd.DataFrame
        A data frame created from the file you provided
    """
    try:
        data = pd.read_csv(f'{name_of_data_folder}/{file_name}')
        return data
    except FileNotFoundError:
        print('data file is not in raw_data folder')
        move_file(file_name, name_of_data_folder)
        data = pd.read_csv(f'{name_of_data_folder}/{file_name}')
        return data
