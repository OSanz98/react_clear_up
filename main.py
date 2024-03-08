# This is a Python project used to clear up node_modules folders in existing react applications
import os
import argparse
import shutil
import errno
import logging
from tqdm import tqdm

# global variable to keep track of total space cleared
total_space_cleared = 0
# store array of errors that we may encounter
errors = []

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')


def get_directory_size(directory):
    """
    Calculates the total size of a directory by recursively walking through its files.
    :param directory: (str) The path to the directory.
    :return: Total size of the directory in bytes.
    """
    total_size = 0
    for directoryPath, directoryNames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(directoryPath, f)
            total_size += os.path.getsize(fp)
    return total_size


def is_react_app(directory):
    """
    Checks if a given directory is a React application by looking for the 'package.json' file.
    :param directory: (str) Path to directory.
    :return: bool - True if directory is a React application, False otherwise.
    """
    package_json_path = os.path.join(directory, 'package.json')
    return os.path.exists(package_json_path)


def remove_node_modules(directory):
    """
    Removes 'node_modules' folder from a given directory and updates the total space cleared.
    :param directory: (str) Path to directory.
    """
    global total_space_cleared  # access global variable
    node_modules_path = os.path.join(directory, 'node_modules')  # store path to the node_modules folder
    if os.path.exists(node_modules_path):  # if exists then remove folder
        try:
            node_modules_size = get_directory_size(node_modules_path)
            shutil.rmtree(node_modules_path)  # remove node_modules folder
            total_space_cleared += node_modules_size  # update total_space_cleared
            logging.info(f"Removed node_modules from {directory}")
        except PermissionError:
            errors.append(f"Error: Permission denied to remove node_modules from {directory}")


def scan_and_clean(root_dirs, skip_dir):
    """
    Recursively scans the root directory and its subdirectories for React applications,
    skipping the directories specified in the 'skip_directories' list, and removes their node_modules folders.
    :param skip_dir: (str[]) Array of paths to skip in clean up
    :param root_dirs: (str) Path to root directory.
    """
    react_apps_found = []
    for root_dir in root_dirs:
        for root, dirs, files in os.walk(root_dir):
            # returns true if both pathname arguments refer to the same file or directory
            if any(os.path.samefile(root, os.path.abspath(directory)) for directory in skip_dir):
                # loops through each file/directory specified in skip directories array to compare against
                continue
            if is_react_app(root):
                react_apps_found.append(root)

    progress_bar = tqdm(total=len(react_apps_found), unit='app', desc='Cleaning React apps')
    for app_path in react_apps_found:
        remove_node_modules(app_path)
        progress_bar.update(1)
    progress_bar.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Clean up React applications")
    parser.add_argument('directories', nargs='+', type=str, help='Root directories to scan')
    parser.add_argument('--skip', nargs='*', default=[], help='Directories or applications to skip')
    args = parser.parse_args()

    root_directories = [os.path.abspath(root_dir) for root_dir in args.directories]
    # Populate the skip_directories list with the directories or applications to skip
    skip_directories = [os.path.abspath(skip_dir) for skip_dir in args.skip]

    scan_and_clean(root_directories, skip_directories)

    # Print the total space cleared
    logging.info(f"Total space cleared: {total_space_cleared} bytes")

    # Print any errors encountered
    if errors:
        logging.info("\nErrors encountered:")
        for error in errors:
            logging.error(error)
