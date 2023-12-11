"""
Functions
---------
move_file
clean
"""
import os
import shutil


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
    # create a new directory
    os.makedirs(folder_name, exist_ok=True)
    # path of the file when moved
    destination_file = os.path.join(folder_name, os.path.basename(file_name))
    try:
        # move the file
        shutil.move(file_name, folder_name)
    except shutil.Error:
        """This error typically occurs when there is already a file with the same name in the 
            destination directory. If this is the case, we fill delete the original file"""

        print(f'{file_name} already exists in {file_name}, now overriding it!')
        os.remove(destination_file)
        # move the file
        shutil.move(file_name, folder_name)
    except FileNotFoundError:
        print(f"Please put the raw data file in the same directory as this python script. "
              f"If you think you have provided the file, please check if the file name is correct.")


def clean():
    """Clean files after computation"""

    # folder name
    data_folder = 'data'
    plots_folder = 'plots'
    pickle_folder = 'pickles'

    # clean files
    for file in os.listdir(os.getcwd()):
        if file.endswith('.csv'):
            move_file(file, data_folder)
        if file.endswith('.png'):
            move_file(file, plots_folder)
        if file.endswith('.pkl'):
            move_file(file, pickle_folder)
