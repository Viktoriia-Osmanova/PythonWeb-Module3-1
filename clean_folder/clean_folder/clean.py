import re
from pathlib import Path
import sys
import shutil
import concurrent.futures

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

jpeg_files = list()
png_files = list()
jpg_files = list()
txt_files = list()
docx_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    "JPEG": jpeg_files,
    "PNG": png_files,
    "JPG": jpg_files,
    "TXT": txt_files,
    "DOCX": docx_files,
    "ZIP": archives
}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name):
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', "_", new_name)
    return f"{new_name}.{'.'.join(extension)}"

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def move_file(file, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    new_path = target_folder / normalize(file.name)
    shutil.move(str(file), str(new_path))

def process_folder(folder_path):
    jpeg_files = []
    jpg_files = []
    png_files = []
    txt_files = []
    docx_files = []
    others = []
    archives = []

    for item in folder_path.iterdir():
        if item.is_dir():
            if item.name not in ("JPEG", "JPG", "PNG", "TXT", "DOCX", "OTHER", "ARCHIVE"):
                sub_folder_files = process_folder(item)
                jpeg_files.extend(sub_folder_files[0])
                jpg_files.extend(sub_folder_files[1])
                png_files.extend(sub_folder_files[2])
                txt_files.extend(sub_folder_files[3])
                docx_files.extend(sub_folder_files[4])
                others.extend(sub_folder_files[5])
                archives.extend(sub_folder_files[6])
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder_path / item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

    return jpeg_files, jpg_files, png_files, txt_files, docx_files, others, archives

def main(folder_path):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        
        
        for item in folder_path.iterdir():
            if item.is_dir():
                futures.append(executor.submit(process_folder, item))

        for future in concurrent.futures.as_completed(futures):
            sub_folder_files = future.result()

            
            jpeg_files.extend(sub_folder_files[0])
            jpg_files.extend(sub_folder_files[1])
            png_files.extend(sub_folder_files[2])
            txt_files.extend(sub_folder_files[3])
            docx_files.extend(sub_folder_files[4])
            others.extend(sub_folder_files[5])
            archives.extend(sub_folder_files[6])

       
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as move_executor:
            move_futures = []

            for file in jpeg_files:
                move_futures.append(move_executor.submit(move_file, file, folder_path, "JPEG"))

            for file in jpg_files:
                move_futures.append(move_executor.submit(move_file, file, folder_path, "JPG"))

            for file in png_files:
                move_futures.append(move_executor.submit(move_file, file, folder_path, "PNG"))

        

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")
    arg = Path(path)
    main(arg.resolve())
