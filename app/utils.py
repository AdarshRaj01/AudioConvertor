import os

def remove_temp_files(files: List[str]):
    for file in files:
        if os.path.exists(file):
            os.remove(file)
