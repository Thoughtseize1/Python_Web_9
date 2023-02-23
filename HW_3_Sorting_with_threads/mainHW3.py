import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread, Semaphore
import logging
from normalize import normalize
import os
import time


parser = argparse.ArgumentParser(
    description="""
Aplication for sorting folder.
python main.py --sourse -s - source folden needed to sort.
python main.py — output -o distanation.
The -n parametr in False by default, but if you need to rename each file to latin symbols you should use this flag

"""
)
# Adding arguments
parser.add_argument(
    "-s",
    "--source",
    help="Source folder which we need to sort",
    required=True,
    default="test_dir",
)  # option that takes a name of folder we need to sort
parser.add_argument("-o", "--output", default="Sorted_folder")
parser.add_argument(
    "-n",
    "--normal",
    action="store_true",
    help="Just use '-n' argument to normalize filenames in created folder",
)
args = vars(parser.parse_args())  # Create arguments to dictionary from object argparse
source = args.get("source")
output = args.get("output")
need_normalize = args.get("normal")


folders = []

# Function for collecting folders
def grabs_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def sorting_copy(path: Path, semaphore: Semaphore):
    with semaphore:
        for el in path.iterdir():
            if el.is_file():
                extention = el.suffix
                new_folder_name = output_folder / extention[1:].upper()
                try:
                    new_folder_name.mkdir(exist_ok=True, parents=True)
                    new_file_name = normalize(el.name) if need_normalize else el.name
                    copyfile(el, new_folder_name / new_file_name)
                except OSError as error:
                    logging.error(error)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    base_folder = Path(source)
    output_folder = Path(output)

    folders.append(base_folder)
    grabs_folder(base_folder)

    pool = Semaphore(2)
    threads = []
    for folder in folders:
        th = Thread(target=sorting_copy, args=(folder, pool))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    logging.debug("Now you can delete source folder")
