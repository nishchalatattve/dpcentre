"""
This is my generic tool box.
Haoze 24

Dependencies
------------
    - pandas

    - project_src

Contents
--------
"""
import pandas as pd
from .projects_src.io import *


def get_data_from(file_name: str, name_of_data_folder='data'):
    """
    Get data from a csv file.

    Description
    -----------
        - read data from a csv file
        - convert all data to numeric

    Parameters
    ----------
    file_name: str
        The name of the file to generate df from.

    name_of_data_folder: str
        The name of the folder containing file_name. Default to data

    Returns
    -------
    numeric_df: pd.DataFrame
        A dataframe in which data is all numeric
    """
    data = None
    try:
        data = pd.read_csv(f'{name_of_data_folder}/{file_name}')
    except FileNotFoundError:
        try:
            data = pd.read_csv(f'{file_name}')
        except FileNotFoundError:
            print(f'File {file_name} not found!')

    numeric_df = pd.DataFrame(data).apply(pd.to_numeric, errors='coerce').dropna()

    return numeric_df
