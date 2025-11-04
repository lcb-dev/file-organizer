import os
import mimetypes
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
            else:
                category = 'Other'
                rows.append([entry.name, 'Other', '', ''])
            
            print(entry.name, '->', category)
    print(tabulate(rows, headers=['Name','Kind','MIME','Category'], tablefmt='github'))

def cat_from_mime(filename, default='Other'):
    mime, _ = mimetypes.guess_type(filename)
    if not mime:
        return default, mime
    top, _, sub = mime.partition('/')
    return TOP_LEVEL_MAP.get(top, default), mime


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