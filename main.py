# This is a Python project used to clear up node_modules folders in existing react applications
import os
import argparse
import shutil

# global variable to keep track of total space cleared
total_space_cleared = 0


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
    global total_space_cleared
    node_modules_path = os.path.join(directory, 'node_modules')
    if os.path.exists(node_modules_path):
        node_modules_size = get_directory_size(node_modules_path)
        shutil.rmtree(node_modules_path) # remove node_modules folder
        total_space_cleared += node_modules_size
        print(f"removed node_modules from {directory}")


def scan_and_clean(root_dir, skip_dir):
    """
    Recursively scans the root directory and its subdirectories for React applications,
    skipping the directories specified in the 'skip_directories' list, and removes their node_modules folders.
    :param skip_dir: (str[]) Array of paths to skip in clean up
    :param root_dir: (str) Path to root directory.
    """
    for root, dirs, files in os.walk(root_dir):
        if any(os.path.samefile(root, os.path.abspath(directory)) for directory in skip_dir):
            continue
        if is_react_app(root):
            remove_node_modules(root)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Clean up React applications")
    parser.add_argument('directory', type=str, help='Root directory to scan')
    parser.add_argument('--skip', nargs='*', default=[], help='Directories or applications to skip')
    args = parser.parse_args()

    root_directory = args.directory
    # Populate the skip_directories list with the directories or applications to skip
    skip_directories = [os.path.abspath(skip_dir) for skip_dir in args.skip]

    scan_and_clean(root_directory, skip_directories)

    # Print the total space cleared
    print(f"Total space cleared: {total_space_cleared} bytes")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
