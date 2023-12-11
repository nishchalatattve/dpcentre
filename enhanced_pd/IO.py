"""
Functions
---------
get_data_from
"""
import pandas as pd


def get_data_from(file_name: str, name_of_data_folder='data'):
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
    data = None
    try:
        data = pd.read_csv(f'{name_of_data_folder}/{file_name}')
    except FileNotFoundError:
        try:
            data = pd.read_csv(f'{name_of_data_folder}/{file_name}')
        except FileNotFoundError:
            print(f'File {file_name} not found!')

    numeric_df = pd.DataFrame(data).apply(pd.to_numeric, errors='coerce').dropna()
    sorted_df = numeric_df.sort_values(numeric_df.columns[0])

    return sorted_df
