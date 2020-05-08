
import os


def create_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def get_all_files(path: str, extension: str='', negative=False):
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            condition = filename.endswith("{}".format(extension))
            if condition ^ negative:
                yield os.path.join(dirpath, filename)

def write_file_safe(path, content):
    directory = os.path.dirname(path)
    create_directory(directory)
    with open(path, 'w') as out_file:
        out_file.write(content)

