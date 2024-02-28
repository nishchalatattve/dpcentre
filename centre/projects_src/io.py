"""
Input and Output operations
Haoze 24

Contents
--------
    - indicate

"""
import os
import shutil


def indicate(indicator_text):
    """Print indicator text"""

    # ANSI escape codes for colors and formatting
    blue = '\033[94m'
    bold = '\033[1m'
    end = '\033[0m'

    # Constructing the string with the desired formatting
    formatted_text = blue + '==>' + end + ' ' + bold + indicator_text + end
    print(formatted_text)


def move_file(file_name: str, folder_name: str):
    os.makedirs(folder_name, exist_ok=True)

    try:
        shutil.move(file_name, folder_name)
    except shutil.Error:
        # This error typically occurs when there is already a file with the same name in the
        # destination directory. If this is the case, we fill delete the original file
        print(f'{file_name} already exists in {folder_name}, now overriding it!')
        destination_file = os.path.join(folder_name, os.path.basename(file_name))
        os.remove(destination_file)
        shutil.move(file_name, folder_name)
    except FileNotFoundError:
        print('Please put the file in the same directory as this python script.')


def clean_plots():
    plots_folder = 'plots'
    for file in os.listdir(os.getcwd()):
        if file.endswith('.png'):
            move_file(file, plots_folder)


def clean_all():
    """Clean files after computation"""

    indicate('cleaning files')

    # folder names
    data_folder = 'data'

    pickle_folder = 'pickles'
    pdf_folder = 'pdfs'
    word_folder = 'MS Word'

    # clean files
    for file in os.listdir(os.getcwd()):
        # if file.startswith('.'):
        #     os.remove(f'{data_folder}/{file}')
        if not file.startswith('.'):
            if file.endswith('.csv'):
                move_file(file, data_folder)
            if file.endswith('.pkl'):
                move_file(file, pickle_folder)
            if file.endswith('.pdf'):
                move_file(file, pdf_folder)
            if file.endswith('.docx'):
                move_file(file, word_folder)

    indicate('finished cleaning!')
