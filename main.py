import os
import mimetypes
import shutil
from enum import Enum
from pathlib import Path
from tabulate import tabulate

TOP_LEVEL_MAP = {
    'image': 'Images',
    'video': 'Videos',
    'audio': 'Audio',
    'text': 'Text',
    'font': 'Fonts',
    'application': None,
    'message': 'Email',
    'multipart': 'Archive'
}

def main(path='.'):
    rows = []
    mime_types = set()
    files_to_move = []
    with os.scandir(path) as d:
        print("Current directory: ")
        print(os.getcwd())
        print("Items in current directory: ")
        for entry in d:
            if(entry.is_dir()):
                category = 'Directory'
                rows.append([entry.name, 'Directory', '', ''])
            elif(entry.is_file()):
                category, mime = cat_from_mime(entry.path)
                rows.append([entry.name, 'File', mime or '', category])
                files_to_move.append((entry.path, category))
            else:
                category = 'Other'
                rows.append([entry.name, 'Other', '', ''])
            
            m_type, _ = cat_from_mime(entry.name)
            mime_types.add(m_type)
            print(entry.name, '->', category)
    print(tabulate(rows, headers=['Name','Kind','MIME','Category'], tablefmt='github'))
    create_sub_directories(mime_types)
    move_files_to_cats(files_to_move)

def cat_from_mime(filename, default='Other'):
    mime, _ = mimetypes.guess_type(filename)
    if not mime:
        return default, mime
    top, _, sub = mime.partition('/')
    return TOP_LEVEL_MAP.get(top, default), mime

def create_sub_directories(unique_mimes: set):
    for item in unique_mimes:
        if not item:
            continue
        try:
            os.makedirs(item)
            print("Created directory: ", item)
        except FileExistsError:
            print(f"Directory '{item}' already exists.")
            pass

def move_files_to_cats(files):
    for filepath, category in files:
        if not category:
            category = 'Other'
        dest_path = os.path.join(category, os.path.basename(filepath))
        try:
            shutil.copy2(filepath, dest_path)
            print(f"Copied {filepath} -> {dest_path}")
        except Exception as e:
            print(f"Failed to copy {filepath}: {e}")

class FileCategory(Enum):
    IMAGE = 1
    VIDEO = 2
    AUDIO = 3
    DOCUMENT = 4
    TEXT = 5
    EXECUTABLE = 6
    OTHER = 7


if __name__ == '__main__':
    main()